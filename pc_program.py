from subprocess import call


class PcProgram:
    def __init__(self):
        pass

    def get(self, name):
        self.open_edge(name)

    def open_edge(self, website):
        if website == None:
            website = ""

        call("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe ")

    def open_chrom(self, website):
        if website == None:
            website = ""

        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + website)
