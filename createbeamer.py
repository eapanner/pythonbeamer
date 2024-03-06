#script that creates a beamer from a textfile with a list of image file paths and associated metadata using pylatex
#see https://jeltef.github.io/PyLaTeX/current/index.html

from pylatex import Document, Section, Subsection, Tabular, Command, Figure, Enumerate
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import  NoEscape
from array import array
import argparse as argparse
import os

#input to command line is a textfile and the name of the output beamer. 
    # eg: python3 makeimagebeamer.py -t imagedata.txt -o slideshow

parser = argparse.ArgumentParser("Make Beamer")
parser.add_argument("-t", "--textfile", required=True, type=str, help="image data")
parser.add_argument("-o", "--outfile", required = True, type = str, help = "outputbeamerfile")
args = parser.parse_args()

#define environments to use column and columns
class Columns(Environment):
    _latex_name = 'columns'

class Column(Environment):
    _latex_name = 'column'

readfile = open(args.textfile, 'r')

#this dictionary will allow us to find the metadata associated with each image later
metadataDict = {}

#examples of categories that could be created based on sorted metadata
trueImages = []
falseImages = []

#read through each line of the input text file
while True:
    line = readfile.readline()
    metadata = []
    if not line:
        break
    
    for word in line.split():
        metadata.append(word)
        
    #the line below assumes that the first entry in each line is the filepath of the image
    imagepath = metadata[0]

    # each entry in the dictionary will save the metadata with the associated filepath.
    metadataDict[imagepath] = metadata
    
    #this is an example of a possible category that could be present in the textfile
    if metadata[2] == "true":
        trueImages.append(imagepath)
    else:
        falseImages.append(imagepath)
    
    
    
#set the geometry options of the document
geometry_options = {"tmargin": ".5cm", "lmargin":".5cm", "margin": ".5cm"}

#create a document of class beamer
doc = Document(geometry_options=geometry_options, documentclass="beamer", fontenc = 'T1', inputenc = 'utf8', font_size= "tiny")



#create a slide for each image in a given list
for image in trueImages:
    doc.create(Section('Slide'))
    
    with doc.create(Columns()):
        with doc.create(Column(arguments=Arguments((NoEscape(r".2\textwidth"))))):
            #create a bulleted list of the metadata for each image
            with doc.create(Enumerate(enumeration_symbol="*",
                                options={})) as enum:
                for data in metadataDict[image]:
                    enum.add_item(data)
        
        with doc.create(Column(arguments=Arguments((NoEscape(r".8\textwidth"))))):
            with doc.create(Figure(position='h!')) as fig_map:
                fig_map.add_image(image, width = '250px')

#Generate the beamer. This uses pdflatex by default.
doc.generate_pdf(args.outfile, clean_tex=False, clean=True)
