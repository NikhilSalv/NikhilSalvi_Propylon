# Interview Test - Oireachtas Api


<img width="886" alt="cover" src="https://github.com/user-attachments/assets/68e03026-d05a-489f-afb1-c230d3a5a349">

# Key Achievements :

<p align="center">
  <img src="https://github.com/user-attachments/assets/0af49d47-e4bb-43b4-bfd2-991441333602" alt="Key Achievements" />
</p>


## Content
- [Assessment Goals](#assessment-goals)
- [User Stories](#user-stories)
    - [Filter Bills Sponsored by a Member](#filter-bills-sponsored-by-a-member)
    - [Filter Bills by Last Updated Date Range](#filter-bills-by-last-updated-date-range)
- [Design and flow](#design-and-flow)
- [Testing write-ups](#testing-write-ups)
    - [PEP8 Validator](#PEP-8-validator)
    - [Unit Testing](#unit-testing)
    - [Logs](#logs)


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

## Design and flow

                Start
                  |
         Enter pId of member
                  |
                  v
      +----------------------------------------+
      |  Call filter_bills_sponsored_by(pId)   |
      +----------------------------------------+
                  |
         Valid pId? (Check)
        /               \
      Yes               No
      |                  |
      v                  v
    Fetch bills     Log error: "No such member..."
    sponsored by    Prompt for valid pId or exit
    the member      (Repeat loop)
      |
      v
    Display bills 
    (bill numbers)
      |
      v
    Enter 'since' 
    and 'until' dates
      |
      v
    Call filter_bills_by_last_updated(since_date_str, until_date_str)
      |
      v
    Validate dates
      |
      v
    Filter bills 
    updated within date range
      |
      v
    Display filtered bills
    (bill numbers)
      |
      v
    End

1. #### filter_bills_sponsored_by(pId: str)

**Purpose:** 

This function retrieves bills sponsored by a specific member identified by their unique member ID (pId). It allows users to understand legislative actions tied to individual members.

**Flow:**

- **Fetch Data:**

> The function starts by calling fetch_data_from_api_with_cache to obtain member and legislation data from the Oireachtas API.
> It creates a dictionary mapping member IDs to their names using create_members_dict.

- **Input Validation:**

> A loop is initiated to check if the provided pId exists in the members_dict.
> If the pId is invalid, the user is prompted to enter a valid ID or exit the process. If the user chooses to exit, the function returns an empty list.
> Upon successful validation, it logs the member ID found.

- **Filter Bills:**

> The function then iterates through the legislation results to collect bills that are sponsored by the identified member.
> It checks if the member's name appears in the sponsors of each bill.
> The filtered list of bills is returned.

- **Output:**

> The result is a list of dictionaries containing details about the bills sponsored by the member.

2. #### filter_bills_by_last_updated(since_date_str: str, until_date_str: Optional[str] = None)

**Purpose:** 

This function filters and returns bills that have been updated within a specified date range. It is essential for tracking recent legislative changes.

**Flow:**

- **Fetch Legislation Data:**

> The function retrieves legislation data using fetch_data_from_api_with_cache.
> It checks if the data was successfully fetched; if not, it returns an empty list.

- **Date Input Handling:**

> The function calls get_valid_date_input for both since_date_str and until_date_str to convert user inputs into date objects.
> If the inputs are invalid, it logs a warning and returns None.

- **Validate Date Range:**

> The dates are validated using validate_date_range, which checks that the 'since' date is not later than the 'until' date.
> If the date range is invalid, a ValueError is raised.

- **Filter Bills:**

> The function initializes an empty list to store bills that match the criteria.
> It iterates through the legislation results, converting the lastUpdated string of each bill into a datetime.date object.
> Each bill is checked to see if its lastUpdated date falls within the specified date range. Matching bills are appended to the filtered list.

- **Output:**

> The function returns the list of bills updated within the specified date range.


## Testing write-ups

- **PEP 8 validator**

<p align="center">
<img width="1397" alt="PEP8" src="https://github.com/user-attachments/assets/c7b97a7c-fcc1-41c2-8153-6cea389b907b">
</p>


<p align="center">
<img width="1348" alt="PEP 8 Fixed" src="https://github.com/user-attachments/assets/e968c1ed-167b-499a-b881-d9240226cf9e" width= "10">
</p>


- **Unit testing**

<p align="center">
<img width="785" alt="unit testing" src="https://github.com/user-attachments/assets/b32e58bb-ab91-45e6-90ab-a96a40b1d62d">
</p>

- ### test_create_members_dict:
> **Purpose:** This test checks the functionality of the create_members_dict function. It validates whether the function correctly transforms the input member_data into the expected dictionary format.
> **Process:**
-A sample member_data dictionary is created with a couple of members.
-The expected output dictionary is defined.
-The function create_members_dict is called with member_data, and its result is compared against the expected output using self.assertEqual(). If they match, the test passes; if not, it fails.

- ### test_validate_date_range:

> **Purpose:** This test verifies that the validate_date_range function correctly handles date range validation.
> **Process:**
-Two datetime objects, since and until, are defined.
-The function is called with these dates, and the result is checked to ensure it returns the same dates as a tuple.
-The test also checks that a ValueError is raised when an invalid date range is provided (i.e., when since is later than until).

- **Logs**
<p align="center">
<img width="840" alt="Logs" src="https://github.com/user-attachments/assets/eee2f942-4374-4a50-ae04-2c7c474c146f">
</p>


