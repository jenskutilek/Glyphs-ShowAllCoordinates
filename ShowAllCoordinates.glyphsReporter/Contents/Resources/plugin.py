# encoding: utf-8

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import ReporterPlugin
from AppKit import NSAttributedString, NSClassFromString, NSColor, NSFont, \
    NSFontAttributeName, NSForegroundColorAttributeName, \
    NSUserDefaults, NSMakeRect, NSNotFound, NSMakePoint

# def angle(p1, p2):
#    return atan2(p2.y - p1.y, p2.x - p1.x)


class ShowAllCoordinates(ReporterPlugin):

    @objc.python_method
    def settings(self):
        self.menuName = Glyphs.localize({
            'en': u'All Coordinates',
            'de': u'Alle Koordinaten'
        })

    def foregroundInViewCoords(self, sender=None):
        layer = self.controller.activeLayer()
        scale = self.getScale()
        position = self.controller.selectedLayerOrigin
        windowController = self.controller.view().window().windowController()
        if windowController:
            tool = windowController.toolDrawDelegate()
            if (
                tool.isKindOfClass_(NSClassFromString("GlyphsToolText"))
                or tool.isKindOfClass_(NSClassFromString("GlyphsToolHand"))
                or tool.isKindOfClass_(NSClassFromString("GlyphsToolTrueTypeInstructor"))
            ):
                return
        if scale < 0.5:
            return
        
        for path in layer.paths:
            for node in path.nodes:
                pt = node.position
                scaledPoint = NSMakePoint(pt.x * scale + position.x, pt.y * scale + position.y)
                # phi = degrees(angle(prev_pt, pt))
                # if phi > 270 or -90 < phi < 90:
                #    textAlignment = 5
                #    # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
                # else:
                #    textAlignment = 3
                self.drawTextAtPoint(
                    " %g, %g" % (pt.x, pt.y),
                    scaledPoint,
                    6
                )
        for anchor in layer.anchors:
            pt = anchor.position
            scaledPoint = NSMakePoint(pt.x * scale + position.x, pt.y * scale + position.y)
            self.drawTextAtPoint(
                " %g, %g" % (pt.x, pt.y),
                scaledPoint,
                6
            )

    # def inactiveLayer(self, layer):
    #     return

    # def preview(self, layer):
    #     return

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    @objc.python_method
    def drawTextAtPoint(self, text, textPosition, textAlignment=3, fontSize=9.0, fontColor=NSColor.brownColor()):
        """
        Use self.drawTextAtPoint("blabla", myNSPoint) to display left-aligned text at myNSPoint.
        """
        try:
            glyphEditView = self.controller.graphicView()
            fontAttributes = {
                NSFontAttributeName: NSFont.labelFontOfSize_(fontSize),
                NSForegroundColorAttributeName: fontColor
            }
            displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
            displayText.drawAtPoint_alignment_visibleInRect_(
                textPosition,
                textAlignment,
                NSMakeRect(NSNotFound, 0, 0, 0)
            )
        except Exception as e:
            self.logToConsole("drawTextAtPoint: %s" % str(e))
