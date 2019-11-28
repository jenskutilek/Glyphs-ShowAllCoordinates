# encoding: utf-8

import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import ReporterPlugin
from AppKit import NSAttributedString, NSClassFromString, NSColor, NSFont, \
    NSFontAttributeName, NSForegroundColorAttributeName, \
    NSUserDefaults

# def angle(p1, p2):
#    return atan2(p2.y - p1.y, p2.x - p1.x)


class ShowAllCoordinates(ReporterPlugin):

    def settings(self):
        self.menuName = Glyphs.localize({
            'en': u'All Coordinates',
            'de': u'Alle Koordinaten'
        })

    def foreground(self, layer):
        currentController = self.controller.view().window().windowController()
        if currentController:
            tool = currentController.toolDrawDelegate()
            if (
                tool.isKindOfClass_(NSClassFromString("GlyphsToolText"))
                or tool.isKindOfClass_(NSClassFromString("GlyphsToolHand"))
                or tool.isKindOfClass_(NSClassFromString("GlyphsToolTrueTypeInstructor"))
            ):
                return
        self.current_zoom = self.getScale()
        if self.current_zoom < 0.5:
            return

        for path in layer.paths:
            for segment in path.segments:
                for pt in segment:
                    # phi = degrees(angle(prev_pt, pt))
                    # if phi > 270 or -90 < phi < 90:
                    #    textAlignment = 5
                    #    # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
                    # else:
                    #    textAlignment = 3
                    self.drawTextAtPoint(
                        " %g, %g" % (pt.x, pt.y),
                        (pt.x, pt.y),
                        6
                    )
                    # prev_pt = pt
        for anchor in layer.anchors:
            self.drawTextAtPoint(
                " %s, %s" % (anchor.position.x, anchor.position.y),
                (anchor.position.x, anchor.position.y),
                6
            )

    # def inactiveLayer(self, layer):
    #     return

    # def preview(self, layer):
    #     return

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    def drawTextAtPoint(self, text, textPosition, textAlignment=3, fontSize=9.0, fontColor=NSColor.brownColor()):
        """
        Use self.drawTextAtPoint("blabla", myNSPoint) to display left-aligned text at myNSPoint.
        """
        try:
            glyphEditView = self.controller.graphicView()
            fontAttributes = {
                NSFontAttributeName: NSFont.labelFontOfSize_(fontSize / self.current_zoom),
                NSForegroundColorAttributeName: fontColor
            }
            displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
            glyphEditView.drawText_atPoint_alignment_(
                displayText,
                textPosition,
                textAlignment
            )
        except Exception as e:
            self.logToConsole("drawTextAtPoint: %s" % str(e))

    def getHandleSize(self):
        """
        Returns the current handle size as set in user preferences.
        Use: self.getHandleSize() / self.getScale()
        to determine the right size for drawing on the canvas.
        """
        try:
            Selected = NSUserDefaults.standardUserDefaults().integerForKey_("GSHandleSize")
            if Selected == 0:
                return 5.0
            elif Selected == 2:
                return 10.0
            else:
                return 7.0  # Regular
        except Exception as e:
            self.logToConsole(
                "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e)
            )
            return 7.0

    def getScale(self):
        """
        self.getScale() returns the current scale factor of the Edit View UI.
        Divide any scalable size by this value in order to keep the same apparent pixel size.
        """
        try:
            return self.controller.graphicView().scale()
        except:
            self.logToConsole("Scale defaulting to 1.0")
            return 1.0
