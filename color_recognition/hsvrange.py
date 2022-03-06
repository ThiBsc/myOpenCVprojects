'''
Represent an HSV value
H is the Hue color
S is the Saturation (greyness)
V is the Value (brightness)
'''
class HsvRange:
    def __init__(self, lowerHSV, upperHSV, label):
        self.lowerHSV = lowerHSV
        self.upperHSV = upperHSV
        self.label = label

    def __str__(self):
        return self.label

    def isInRange(self, hsvColor):
        # print('isInRange', hsvColor, self.lowerHSV, self.upperHSV)
        inHue = self.lowerHSV[0] <= hsvColor[0] <= self.upperHSV[0]
        inSaturation = self.lowerHSV[1] <= hsvColor[1] <= self.upperHSV[1]
        inValue = self.lowerHSV[2] <= hsvColor[2] <= self.upperHSV[2]
        return inHue and inSaturation and inValue