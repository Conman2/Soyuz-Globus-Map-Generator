# Plan to generate a replica of the soyuz globus map.
# Elements required:
# 1. Terrain Topology (Stylised)
# 2. Grid Overlay 
# 3. Landing Sights? 
# 4. Towns 
# 5. Rivers

# Fix Grid Line projection (apply to horiizontal lines)

from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from PIL import ImageFont

import pandas

#Vars 
img_height = 2700
img_width = 5400

#Displacement Map Refernce
DisplacementMap = Image.open("EARTH_DISPLACE_5K_16BITS.jpg")
DisplacementMap = DisplacementMap.filter(ImageFilter.GaussianBlur(3))

Borders = Image.open("Borders.png")

#Dont think this made up thing works properly, who would of guessed
def EquiRectangularProjection(img_height, pix_height):
    equator = img_height/2
    distance_to_equator = abs(equator - pix_height)
    deformation = (equator - pow(pow(equator, 2) - pow(distance_to_equator, 2), 0.5))
    return deformation

def LongLatToXY(longitude, latitude, image_height, image_width):
    x = (((float(longitude) - -180) * (image_width - 0)) / (180 - -180)) + 0
    y = (((-float(latitude) - -90) * (image_height - 0)) / (90 - -90)) + 0
    return x,y

# Creat the Terrain texture 
Texture = Image.new(mode="RGBA", size=(img_width, img_height))

for i in range(0, img_width):
    for j in range(0, img_height):

        #Antarctica Test
        if j <= 2250 and j >= 425:
            #Water 
            if DisplacementMap.getpixel((i,j)) < 34: 
                Texture.putpixel((i, j), (131, 166, 186, 255))
            #Terrain 1
            elif DisplacementMap.getpixel((i,j)) < 75:
                Texture.putpixel((i, j), (206, 201, 195, 255))
            #Terrain 2
            elif DisplacementMap.getpixel((i,j)) < 125:
                Texture.putpixel((i, j), (218, 174, 147, 255))
            #Terrain 3
            else:
                Texture.putpixel((i, j), (219, 134, 80, 255))

        elif j > 2250:
            if DisplacementMap.getpixel((i,j)) < 34: 
                Texture.putpixel((i, j), (131, 166, 186, 255))    
            else:
                Texture.putpixel((i, j), (244, 244, 244, 255))  
            
        elif j < 425:
            if DisplacementMap.getpixel((i,j)) < 34: 
                Texture.putpixel((i, j), (131, 166, 186, 255))    
            else:
                Texture.putpixel((i, j), (125, 157, 182, 255))  

#Coast Outline
Coast = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))   
for i in range(0, img_width):
    for j in range(0, img_height):
        if DisplacementMap.getpixel((i,j)) < 34:
            Coast.putpixel((i, j), (33, 69, 103, 255))   
Coast = Coast.filter(ImageFilter.FIND_EDGES) 

#Terrain Outline
Terrain1 = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))   
for i in range(0, img_width):
    for j in range(0, img_height):
        if j > 425 and j < 2250 and DisplacementMap.getpixel((i,j)) > 75:
                Terrain1.putpixel((i, j), (145, 126, 111, 255))   
Terrain1 = Terrain1.filter(ImageFilter.FIND_EDGES) 

Terrain2 = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))   
for i in range(0, img_width):
    for j in range(0, img_height):
        if j > 425 and j < 2250 and DisplacementMap.getpixel((i,j)) > 125:    
             Terrain2.putpixel((i, j), (145, 126, 111, 255))          
Terrain2 = Terrain2.filter(ImageFilter.FIND_EDGES) 

#Towns 
Towns = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))
TownsDrawing = ImageDraw.Draw(Towns)
TownList = pandas.read_excel("simplemaps_worldcities_basicv1.77\worldcities.xlsx")
circle_size = 8

for i in range(1, 200):
    long = TownList.iloc[i+1, 3]
    town_x, town_y = LongLatToXY(TownList.iloc[i, 3], TownList.iloc[i, 2], img_height, img_width)
    TownsDrawing.ellipse([town_x - circle_size, town_y - circle_size, town_x + circle_size, town_y + circle_size], fill = (0,0,0,0), outline = (0,0,0,255), width = 4)
    #TownsDrawing.text((i*img_width/6, img_height/16*10+circle_size/2 - circle_size/1.5), "20", font = font, fill = (0,0,0,255), anchor="mb")

#Rivers (Rate Of Change?)
'''
Rivers = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))

for i in range(1, img_width - 1):
    for j in range(1, img_height - 1):
        Avg = (DisplacementMap.getpixel((i-1, j)) + DisplacementMap.getpixel((i+1,j)) + DisplacementMap.getpixel((i,j-1)) + DisplacementMap.getpixel((i,j+1))) / 4
        Dif = abs(Avg - DisplacementMap.getpixel((i,j)))

        if Dif > 0.5:
            Rivers.putpixel((i, j), (0, 0, 0, 255))
#Rivers.show()
'''

#Lakes
Lakes = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0))

for i in range(1, img_width - 1):
    for j in range(1, img_height - 1):
        if DisplacementMap.getpixel((i,j)) < 50:
             Lakes.putpixel((i, j), (0, 0, 0, 255))

#Circles with numbers
NumberedCircles = Image.new(mode="RGBA",size=(img_width,img_height), color=(255, 255, 255, 0))
NumberedCirclesDrawing = ImageDraw.Draw(NumberedCircles)
circle_size = 40

circle_1_loc = img_height/16*10 - circle_size/1.5
circle_2_loc = img_height/16*12 - circle_size/1.5
circle_3_loc = img_height/16*14 - circle_size/1.5

font = ImageFont.truetype("arial.ttf", 50)

for i in range(0,7):
    #deform_fact_1 = EquiRectangularProjection(img_height, circle_1_loc)
    #deform_fact_2 = EquiRectangularProjection(img_height, circle_2_loc)
    #deform_fact_3 = EquiRectangularProjection(img_height, circle_3_loc)

    width_1 = circle_size #+ circle_size * deform_fact_1 * deform_fact_1 * 2
    width_2 = circle_size #+ circle_size * deform_fact_2 * deform_fact_2 * 2
    width_3 = circle_size #+ circle_size * deform_fact_3 * deform_fact_3 * 2

    NumberedCirclesDrawing.ellipse([i*img_width/6 - width_1, circle_1_loc - circle_size, i*img_width/6 + width_1, circle_1_loc + circle_size], fill = (255,255,255,255), outline = (0,0,0,255), width = 4)
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*10+circle_size/2 - circle_size/1.5), "20", font = font, fill = (0,0,0,255), anchor="mb")
   
    NumberedCirclesDrawing.ellipse([i*img_width/6 - width_2, circle_2_loc - circle_size, i*img_width/6 + width_2, circle_2_loc + circle_size], fill = (255,255,255,255), outline = (0,0,0,255), width = 4)
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*12+circle_size/2 - circle_size/1.5), "40", font = font, fill = (0,0,0,255), anchor="mb")
   
    NumberedCirclesDrawing.ellipse([i*img_width/6 - width_3, circle_3_loc - circle_size, i*img_width/6 + width_3, circle_3_loc + circle_size], fill = (255,255,255,255), outline = (0,0,0,255), width = 4)
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*14+circle_size/2 - circle_size/1.5), "60", font = font, fill = (0,0,0,255), anchor="mb")

#More numbers 
for i in range(0, 7):
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*6 + circle_size/2 + circle_size/1.5), "20", font = font, fill = (0,0,0,255), anchor="mb")
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*4 + circle_size/2 + circle_size/1.5), "40", font = font, fill = (0,0,0,255), anchor="mb")
    NumberedCirclesDrawing.text((i*img_width/6, img_height/16*2 + circle_size/2 + circle_size/1.5), "60", font = font, fill = (0,0,0,255), anchor="mb")

#NumberedCircles.show()
#NumberedCircles.save("Circles.PNG")

#More More Numbers
HorizontalNumbers = Image.new(mode="RGBA",size=(img_width,img_height), color=(255, 255, 255, 0))
HorizontalNumbersDrawing = ImageDraw.Draw(HorizontalNumbers)
for i in range(0,25):
    lat = i + 12
    if lat >= 24:
        lat -= 24

    number = str(lat * 15)

    HorizontalNumbersDrawing.text((i*img_width/24, img_height/16*6 + circle_size/2 - circle_size/1), number, font = font, fill = (0,0,0,255), anchor="mb")
    HorizontalNumbersDrawing.text((i*img_width/24, img_height/16*10 + circle_size/2 + circle_size/1), number, font = font, fill = (0,0,0,255), anchor="mb")

#Grid
Grid = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255, 0) )
GridDrawing = ImageDraw.Draw(Grid)
spacing_y = img_width/24
spacing_x = img_height/16
line_width = 3

#Longitunal Lines
for i in range(0, img_height):
    deform_fact = EquiRectangularProjection(img_height, i)
    width = line_width + line_width * deform_fact * 0.01

    for j in range(0, 25):
        if j % 6 != 0:
            if i > 75 and i < 2624:
                GridDrawing.line([(spacing_y*j - width/2, i),(spacing_y*j + width/2, i)], fill =(11, 29, 43, 255), width = 1)
        else:
            GridDrawing.line([(spacing_y*j - width/2, i),(spacing_y*j + width/2, i)], fill =(11, 29, 43, 255), width = 1)

#Lat Lines
for j in range(0, 17):
    GridDrawing.line([(0, spacing_x*j),(5399, spacing_x*j)], fill =(11, 29, 43, 255), width = 3)

#Ruler Lines
for i in range(0, 16*24):
    GridDrawing.line([(i * img_width/(16*24), img_height/16*6),(i * img_width/(16*24), img_height/16*6 - 15)], fill = (11, 29, 43, 255), width = 2)
    GridDrawing.line([(i * img_width/(16*24), img_height/16*8),(i * img_width/(16*24), img_height/16*8 - 15)], fill = (11, 29, 43, 255), width = 2)
    GridDrawing.line([(i * img_width/(16*24), img_height/16*10),(i * img_width/(16*24), img_height/16*10 + 15)], fill = (11, 29, 43, 255), width = 2)
#Grid.show()

#Composite 
FinalMap = Image.new(mode="RGBA", size=(img_width, img_height))
FinalMap = Image.alpha_composite(FinalMap, Texture) 
#FinalMap = Image.alpha_composite(FinalMap, Borders)
FinalMap = Image.alpha_composite(FinalMap, Coast) 
FinalMap = Image.alpha_composite(FinalMap, Terrain1) 
FinalMap = Image.alpha_composite(FinalMap, Terrain2) 
FinalMap = Image.alpha_composite(FinalMap, Towns) 
FinalMap = Image.alpha_composite(FinalMap, HorizontalNumbers)
FinalMap = Image.alpha_composite(FinalMap, NumberedCircles)
FinalMap = Image.alpha_composite(FinalMap, Grid) 

FinalMap.show()
FinalMap.save("Map.PNG")
