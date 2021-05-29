# MaterialExtractor

This script is used to extract the material data for a category of materials from the free online library "Matweb" eg High Carbon Steels

To extract data from a particular category of materials, just replace the URL in material_class.py file

For eg to extract the properties of materials under the category 'High carbon steels' , the follwoing URL can be used

http://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=249'


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

A simplified Functionality of the code:

> Go to the URL mentioned above and get the individual links for all the materials mentioned on that page

> After getting the individual links for all the materials, go to these individual pages and extract all the data in the table given there.

> Clean up the data and assign it to a dictionary containing data for all the individual materials

> Using, Ultimate Tensile Strength, Yield Strength, Youngs Modulus and Elongation at break , calculate the Ramberg Osgood Coefficent for each material

> Use the Rampberg Osgood Coeff to obtain strains at differnt stress levels. Store the stresses and strain for the individual material in an array

> Create a CSV file for each individual material. This can later be imported in any preprocessor to assign material properties for assigning material properties
