#!/usr/bin/conf
# -*- coding: UTF-8 -*-

hexadecimal = ["#", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]


class Colour:

    def __init__(self, *args):

        if len(args) == 1 \
                and hasattr(args[0], '__iter__') \
                and len(args[0]) == 3 \
                and all(isinstance(n, float) for n in args[0]) \
                and all(0.0 <= n <= 1.0 for n in args[0]):

            self.colour = [a for a in args[0]]
            self.cType = "rgb"

        elif len(args) == 3 \
                and all(isinstance(n, float) for n in args) \
                and all(0.0 <= n <= 1.0 for n in args):

            self.colour = [a for a in args]
            self.cType = "rgb"

        elif len(args) == 1 \
                and isinstance(args[0], float) \
                and 0.0 <= args[0] <= 1.0:

            self.colour = [args[0], args[0], args[0]]
            self.cType = "rgb"

        elif len(args) == 1 \
                and hasattr(args[0], '__iter__') \
                and len(args[0]) == 3 \
                and all(isinstance(n, int) for n in args[0]) \
                and all(0 <= n <= 255 for n in args[0]):

            self.colour = [a for a in args[0]]
            self.cType = "rgb255"

        elif len(args) == 3 \
                and all(isinstance(n, int) for n in args) \
                and all(0 <= n <= 255 for n in args):

            self.colour = [a for a in args]
            self.cType = "rgb255"

        elif len(args) == 1 \
                and isinstance(args[0], int) \
                and 0 <= args[0] <= 255:

            self.colour = [args[0], args[0], args[0]]
            self.cType = "rgb255"

        elif len(args) == 1 \
                and isinstance(args[0], str) \
                and args[0][0] == "#" \
                and len(args[0]) == 7 \
                and all(char.lower() in hexadecimal for char in args[0]):

            self.colour = args[0]
            self.cType = "hex"

        elif len(args) == 1 \
                and hasattr(args[0], '__iter__') \
                and isinstance(args[0][0], int) \
                and 1 < args[0][0] < 255 \
                and 0.0 < args[0][1] < 1.0 \
                and 0.0 < args[0][2] < 1.0:
            self.colour = args[0]
            self.cType = "hsv"

        elif len(args) == 3 \
                and isinstance(args[0], int) \
                and 1 < args[0] < 255 \
                and 0.0 < args[1] < 1.0 \
                and 0.0 < args[2] < 1.0:
            self.colour = [args[0],args[1],args[2]]
            self.cType = "hsv"

        else:
            raise TypeError(
                "Needs Input in form rgb(1.0, 1.0, 1.0),"
                " rgb255(255, 255, 255), hsv(255, 0.0, 0.0)"
                " as args or list of len == 3: or hex(\"#FFFFFF\")"
                " or Finally as hsv (255,1.0,1.0)"
            )

    def __repr__(self):

        if hasattr(self, 'cType') and self.cType:

            return "mc.%s(%s, type='%s')" % (
                self.__class__.__name__, str(self.colour).replace("[", "(").replace("]", ")"), self.cType)

        else:

            return "mc.%s(%s)" % (self.__class__.__name__, str(self.colour))

    def toRGB(self):

        if self.cType == "rgb255":

            self.colour = [round(float(rgb) / 255.0, 4) for rgb in self.colour]

            self.cType = "rgb"

            return self.colour

        elif self.cType == "hex":
            self.colour = [
                round(float(int("0x%s" % self.colour[1:3], 16)) / 255, 4),
                round(float(int("0x%s" % self.colour[3:5], 16)) / 255, 4),
                round(float(int("0x%s" % self.colour[5:7], 16)) / 255, 4)
            ]

            self.cType = "rgb"

            return self.colour

        elif self.cType == "hsv":
            self.fromHSV()

            self.colour = [round(float(rgb) / 255.0, 4) for rgb in self.colour]

            self.cType = "rgb"

            return self.colour

        else:
            return self.colour

    def toRGB255(self):

        if self.cType == "rgb":

            self.colour = [int(rgb * 255) for rgb in self.colour]

            self.cType = "rgb255"

            return self.colour

        elif self.cType == "hex":
            self.colour = [
                int("0x%s" % self.colour[1:3], 16),
                int("0x%s" % self.colour[3:5], 16),
                int("0x%s" % self.colour[5:7], 16)
            ]
            self.cType = "rgb255"

            return self.colour

        elif self.cType == "hsv":

            self.fromHSV()

            self.cType = "rgb255"

            return self.colour


        else:
            return self.colour

    def toHex(self):

        if self.cType == "rgb":
            self.colour = "#{:02x}{:02x}{:02x}".format(int(self.colour[0] * 255),
                                                       int(self.colour[1] * 255),
                                                       int(self.colour[2] * 255))
            self.cType = "hex"

            return self.colour

        elif self.cType == "rgb255":

            self.colour = "#{:02x}{:02x}{:02x}".format(int(self.colour[0]), int(self.colour[1]), int(self.colour[2]))

            self.cType = "hex"

            return self.colour

        elif self.cType == "hsv":

            self.fromHSV()

            self.colour = "#{:02x}{:02x}{:02x}".format(int(self.colour[0]), int(self.colour[1]), int(self.colour[2]))

            self.cType = "hex"

            return self.colour

        else:
            return self.colour

    def toHSV(self):

        if self.cType != "hsv":

            self.toRGB()
            R = self.colour[0]

            G = self.colour[1]

            B = self.colour[2]

            cMax = max(self.colour)

            cMin = min(self.colour)

            delta = cMax - cMin

            if delta == 0:
                H = 0

            elif cMax == R:
                H = 60 * (((G - B) / delta) % 6)

            elif cMax == G:
                H = 60 * (((B - R) / delta) + 2)

            elif cMax == B:
                H = 60 * (((R - G) / delta) + 4)

            else:
                H = 0

            if cMax != 0:
                S = delta / cMax
            else:
                S = 0

            V = cMax

            self.colour = [int(H), round(S, 2), round(V, 2)]
            self.cType = "hsv"

            return self.colour

    def fromHSV(self):

        if self.cType == "hsv":

            H = self.colour[0]
            S = self.colour[1]
            V = self.colour[2]

            C = V * S
            X = C * (1 - abs(((float(H) / 60.00) % 2) - 1))
            m = V - C

            if 0 <= H < 60:
                RGB0 = [C, X, 0]

            elif 60 <= H < 120:
                RGB0 = [X, C, 0]

            elif 120 <= H < 180:
                RGB0 = [0, C, X]

            elif 180 <= H < 240:
                RGB0 = [0, X, C]

            elif 240 <= H < 300:
                RGB0 = [X, 0, C]

            elif 300 <= H < 360:
                RGB0 = [C, 0, X]

            else:
                RGB0 = [0, 0, 0]

            self.colour = [int((RGB0[0] + m) * 255), int((RGB0[1] + m) * 255), int((RGB0[2] + m) * 255)]

            self.cType = "rgb255"

            return self.colour

        else:

            self.toRGB255()

            return self.colour

    @classmethod
    def toQTRGB(cls, r, g, b):

        colourIn = cls(r, g, b).toRGB255()

        return "rgb(%s, %s, %s)" % (colourIn[0], colourIn[1], colourIn[2])
