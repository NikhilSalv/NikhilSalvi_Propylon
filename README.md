# Interview Test - Oireachtas Api

This project has a python module `oireachtas_api` which defines 3 functions to
load and process a couple of the [Houses of the Oireachtas Open Data APIs][1].

Specifically, they use the data obtained from the `legislation` and `members`
api endpoints to answer the questions:

* Which bills were sponsored by a given member ?
* Which bills were last updated within a specified time period ?

You are tasked with doing one or more of the following in any order you are
comfortable with. Obviously the more you manage to get done, the better.

1. The current implementation loads previously obtained offline copy of the data
   obtained from the endpoints. Update the module to fetch the latest data from
   the api endpoint if the parameter passed is the URL to the endpoint instead
   of a filename.

2. The current implementation of the `filter_bills_sponsored_by` appears to be
   correct. It is also reasonably quick when processing the offline data.
   However, when the complete dataset obtained from the api is loaded, it is
   noticeably slower. Refactor the implementation to be faster than the current
   inefficient implementation.

3. Provide an implementation for the unimplemented function
   `filter_bills_by_last_updated`. The specification for this is documented int
   he function's doc-string.

4. Improve the code base as you would any professional quality code. This
   includes not just error checking and improving code readability but also
   adding doc-strings, comments where necessary, additional tests if any ...etc.

Feel free to ask any questions or clarifications, if required.

Wish you the best of luck !

[1] https://api.oireachtas.ie/
