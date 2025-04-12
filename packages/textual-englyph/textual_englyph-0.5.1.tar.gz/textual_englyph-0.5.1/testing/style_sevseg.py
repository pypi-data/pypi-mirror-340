"""Boilerplate code for testing purposes"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual_englyph import EnGlyphText, EnSevSeg


class Test(App):
    """Test console markup styling the englyph text use case"""
    DEFAULT_CSS="""
    #clock {
        margin: 1;
        #hours {
            border-right: none;
        }
        #minutes {
            border-left: none;
        }
        #colon {
            color: red;
            background: #400000;
            border-top: outer black;
            border-bottom: outer black;
        }
    }
    """

    def compose(self) -> ComposeResult:
        """Display seven segment digits. Can use Latin basic characters or
        8 bit direct segment control in PUA \uED00 - \uEDFF
        where 1<<0 (LSB) is segement a, 1<<2 is b, ..., 1<<7 is g and 1<<8 is DP
        """
        yield EnSevSeg("Hello Textual")
        yield EnSevSeg("\uEDCF \uED06 4 1 5")
        with Horizontal(id="clock"):
            yield EnSevSeg("12", id="hours")
            yield EnGlyphText(":", text_size="small", id="colon")
            yield EnSevSeg("34", id="minutes")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
