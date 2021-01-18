
num = 2831
for idx in range(0,num,5):
    imageColourStep=(255*10)/(num)
    colourVal=int(idx*imageColourStep)

    if (colourVal-255<0): # 1
        r = colourVal
        g=0
        b=0
    else:
        colourVal-=255
        if (colourVal-255<0): # 2
            r=0
            g = colourVal
            b=0
        else:
            colourVal-=255
            if (colourVal-255<0): # 3
                r = 0
                g=0
                b = colourVal
            else:
                colourVal-=255
                if (colourVal-255<0): # 4
                    r = colourVal
                    g = 255 
                    b = 0
                else: 
                    colourVal-=255
                    if (colourVal-255<0): # 5
                        r = colourVal
                        g = 0 
                        b = 255
                    else:
                        colourVal-=255
                        if (colourVal-255<0): # 6
                            r = 255 
                            g = colourVal
                            b = 0
                        else:
                            colourVal-=255
                            if (colourVal-255<0): # 7
                                r = 0
                                g = colourVal
                                b = 255
                            else:
                                colourVal-=255
                                if (colourVal-255<0): # 8
                                    r = 255
                                    g = 0
                                    b = colourVal
                                else: 
                                    colourVal-=255
                                    if (colourVal-255<0): # 9
                                        r = 0
                                        g = 255
                                        b = colourVal
                                    else:
                                        colourVal-=255
                                        if (colourVal-255<0): # 10
                                            r = colourVal
                                            g = 255
                                            b = 255
                                        else:
                                            colourVal-=255
                                            if (colourVal-255<0): # 11
                                                r = 255
                                                g = colourVal
                                                b = 255
                                            else:
                                                colourVal-=255
                                                if (colourVal-255<0): # 12
                                                    r = 255
                                                    g = 255
                                                    b = colourVal
                                                else:
                                                    r = 255
                                                    g = 255
                                                    b = 255
    print(r,g,b)