"use strict";

const $ = (element) => document.querySelector(element);

const $button = $("#BTN");
const $stop = $("#stopBTN");
const $text = $(".text");

let isRecording = false;
let stream;
let rec;
let blobs;

const EVENTS = {
  rec: () => {
    $button.classList.add("d-none");
    $stop.classList.remove("d-none");
  },
  stopRec: () => {
    $stop.classList.add("d-none");
    $button.classList.remove("d-none");
  },
};

function recordingChangeText(text, event) {
  isRecording = !isRecording;
  $text.innerText = text;

  event();
}

async function onRecording() {
  try {
    if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
      return new Error("Not user media device");
    }

    blobs = [];

    stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: false,
    });

    rec = new MediaRecorder(stream);

    rec.ondataavailable = (e) => {
      if (e.data) {
        blobs.push(e.data);
      }
    };

    rec.onstop = doStop;

    rec.start();
    recordingChangeText("Recording", EVENTS.rec);
  } catch (e) {
    alert("Error recording: " + e.message);
  }
}

function doStop() {
  if (!blobs.length) {
    return new Error("No blobs");
  }

  const blob = new Blob(blobs);

  let formData = new FormData();

  formData.append("audio", blob, "audio");

  fetch("http://127.0.0.1:3000/audio", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then(handleResponseAudio)
    .catch((err) => console.error(err));
}

function handleResponseAudio(response) {
  if (!response || response == null) {
    return;
  }

  let $response = $(".response");

  $response.textContent = response.text;

  if (typeof response.file !== "undefined") {
    let audioFile = response.file;

    playAudio(audioFile);
  }
}

function playAudio(audioFileName) {
  let audio = new Audio();

  audio.setAttribute("src", "static/" + audioFileName);
  audio.play();
}

function stopListener() {
  rec.stop();
  recordingChangeText("Click to start recording", EVENTS.stopRec);
}

$button.addEventListener("click", onRecording);
$stop.addEventListener("click", stopListener);

document.body.addEventListener("keypress", (e) => {
  if (e.code == "Space") {
    if (!isRecording) {
      onRecording();
    } else {
      stopListener();
    }
  }
});
