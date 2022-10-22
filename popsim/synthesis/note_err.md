# Some common errors and how to fix them

## Key error with the id of a zone

This happens when there is a zone inside the geo_cross_walk that does not exist in the seed data. For example in the case of Melbourne, the zone 299 and 297 (SA4) were dropped.

## Float division by zero

Same reason as above, can work around by delete the zones in geo_cross_walk that does not exist in the seed data. However in this case of Victoria I already solved the SA4 (with merging and deleting 299 and 297), I simply put the seed zone to be SA4