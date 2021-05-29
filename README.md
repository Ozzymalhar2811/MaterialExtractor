# MaterialExtractor

This script is used to extract the material data for a category of materials from the free online library "Matweb" eg High Carbon Steels

To extract data from a particular category of materials, just replace the URL in material_class.py file

For eg to extract the properties of materials under the category 'High carbon steels' , the follwoing URL can be used

http://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=249'

## Libraries Used
> math
> requests
> BeautifulSoup

%%%-------------------------------------------------------------------------------------------------------------------------------------%%%

A simplified Functionality of the code:

> Go to the URL mentioned above and get the individual links for all the materials mentioned on that page

> After getting the individual links for all the materials, go to these individual pages and extract all the data in the table given there.

> Clean up the data and assign it to a dictionary containing data for all the individual materials

> Using, Ultimate Tensile Strength, Yield Strength, Youngs Modulus and Elongation at break , calculate the Ramberg Osgood Coefficent for each material

> Use the Rampberg Osgood Coeff to obtain strains at differnt stress levels. Store the stresses and strain for the individual material in an array

> Create a CSV file for each individual material. This can later be imported in any preprocessor to assign material properties for assigning material properties

%%%-------------------------------------------------------------------------------------------------------------------------------------%%%

## Files : 

> scrapper_main.py: The main file used for importing the class and creating its object
> material_class.py: Functions defined in the class are under this file

## How to run the script:

> Make sure both the files are in the same directory
> In the command prompt enter "python scrapper_main.py" and hit Enter.
> While the script is running you will see which materials are being extracted and which material curves have been made
> You will find the csv files being generated in the same directory