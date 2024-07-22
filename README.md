# Analysis of solar permits in single-family homes in the US

This repo contains the summary the work I did from June'23 - Feb '24 with [Prof. Kim Wolske](https://epic.uchicago.edu/people/kim-wolske/) at the Energy Policy Institute at University of Chicago. 

## Problem: 
NREL breaks down rooftop solar installation costs into two buckets: hardware and _soft costs_. While hardware costs have come down in the last decade, soft costs haven't. A big chunk of these soft costs are _marketing and outreach_, which are high because solar installations are retrofits. DoE wanted to understand what might it take for home builders to move away from a retrofitting approach and install panels at the time of constructing the house. 

## Approach:
Our project involved two components:
 1. Finding out the biggest home builders in the US 
 2. Understanding decision-making of home builder employees on rooftop solar through qualitative surveys

## Contributions:
 1. On part 1, I helped with:
    * Consolidating ~300 big builders across 3 different data sources using pandas 
    * Mapping home permits with these builders using record-linkage algorithms (cosine similarity and Jaro Winkler)
    * Assessing which of these home permits can be classified as _rooftopsolar_ (using a simple bag-of-words approach)

 2. On part 2, my contributions were: 
    * Expanding the list of respondents by fetching data from Google Maps APIs, scraping data from builder websites 
    * Providing feedback on language of questions, co-conducting interviews, making notes

## Documentation:
A big part of this project was maintaining proper documentation. See some examples here:
1. [Using record linkage algorithms for matching builder names](https://github.com/bhoenlbl/PhoenixDataRepo/issues/41)
2. [Identifying solar permits tagged to production builders](https://github.com/bhoenlbl/PhoenixDataRepo/issues/66)

**Code samples available upon request!**