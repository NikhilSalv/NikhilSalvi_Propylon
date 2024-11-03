# Interview Test - Oireachtas Api

<img width="886" alt="cover" src="https://github.com/user-attachments/assets/68e03026-d05a-489f-afb1-c230d3a5a349">

## Content
- [Assessment Goals](#assessment-goals)
- [User Stories](#user-stories)
    - [Filter Bills Sponsored by a Member](#filter-bills-sponsored-by-a-member)
    - [Filter Bills by Last Updated Date Range](#filter-bills-by-last-updated-date-range)


## Assessment goals

This project has a python module `oireachtas_api` which defines 3 functions to
load and process a couple of the [Houses of the Oireachtas Open Data APIs][1].


Specifically, they use the data obtained from the `legislation` and `members`
api endpoints to answer the questions:

- **Which bills were sponsored by a given member ?**
- **Which bills were last updated within a specified time period ?**

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

## User stories

### Filter Bills Sponsored by a Member


> <img width="891" alt="User story one" src="https://github.com/user-attachments/assets/e5873cda-8a2d-4fa7-ae32-8fd6958090d0" width="50">


- As a user of the legislative data system, I want to retrieve a list of bills sponsored by a specific member using their unique pId,
so that I can analyze the contributions and legislative activities of that member.

#### <u>Acceptance Criteria</u>
- The function filter_bills_sponsored_by accepts a pId as input.
- If the pId is valid and exists in the members' dataset, the function returns a list of bills sponsored by that member.
- If the pId is not valid, the user is prompted to enter a valid pId or choose to exit the process.
- If the user chooses to exit, the function terminates gracefully with an empty list.
- The function logs an error if the pId is not found and logs an info message once a valid pId is confirmed.
- The function relies on cached data from API endpoints for both members and legislation.

#### Example Scenario:

- Given the pId "MickBarry" is input,
- When "MickBarry" is found in the members' data,
- Then the function returns a list of bills sponsored by the member with pId "MickBarry".
- If "MickBarry" is not found, the user is prompted to re-enter the pId or exit the process.

### Filter Bills by Last Updated Date Range

<img width="1095" alt="User Striy 2" src="https://github.com/user-attachments/assets/a87b6743-3f54-4e75-985a-e14c287e22a3">

- As a legislative data analyst, I want to filter bills based on the date they were last updated, so that I can review legislative changes and updates within a specific time range for analysis and reporting.

#### <u>Acceptance Criteria</u>

- The function filter_bills_by_last_updated accepts since_date_str (required) and until_date_str (optional) as input parameters.
- If until_date_str is not provided, the function defaults until_date to today's date.
- If the date format for since_date_str or until_date_str is invalid, the function logs a warning and exits, returning None.
- The function validates the date range, ensuring since_date is not later than until_date.
- The function returns a list of bills whose lastUpdated date falls within the specified date range.
- If no bills match the criteria or if an error occurs during data fetching, an empty list is returned.

#### Example Scenario:

- Given the since_date_str "2024-01-01" and until_date_str "2024-06-01" are input,
- When the lastUpdated dates of bills are checked,
- Then the function returns a list of bills updated between January 1, 2024, and June 1, 2024.
- If the since_date_str is invalid or no valid data is fetched, the function exits and returns None.

