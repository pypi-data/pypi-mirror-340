# WebEngage Migration Tool

A lightweight tool to migrate historical user or event data into WebEngage ecosystem.  Supports large datasets and can handle millions of rows, automatic batching, and adhere to WebEngage API rate limits.

---

## Features

- Handles large files efficiently (2M+ rows)
- Batches events or users into groups of 25 adhering API rate limits
- Supports multiple datacenter routing (in, ksa, us)
- Built-in logger for tracking batch status - (success / failure) 

---

## Instructions

- Data should always be in **CSV** format for both **events** and **users**.

- **Delete the first column ("converted JSON")** before saving the file if you plan to **resend** the data to WebEngage.

    #### Sending Users

    - **Column 4**: Reserve this column for Date of Birth. The header name should be **"birthDate"**
    
    - **Columns 1 to 11**: should contain the following fields: **userId**, **firstName**, **lastName**, **birthDate**, **gender**, **email**, **phone**, **company**, **city**, **region**, **country** You can shuffle these columns except for **birthDate**, which will always remain in **column 4**
    
    - **birthDate** values should follow this format: `yyyy-mm-dd` (eg: 1999-12-25)
    
    - **Columns 12 onwards** will contain **custom user attributes**.


    #### Sending Events

    - **Columns 1 to 3**: should contain the following fields: **userId**, **eventName**, **eventTime**. Shuffling of the columns is allowed within this range.

    - **eventTime** should follow this format: `yyyy-mm-ddTHH:MM:SS-0800` (eg: 1986-08-19T15:45:00-0800).

    - **Columns 4 onwards** will contain **event data**.

---

## Installation


To install the package run:

<pre style="font-size: 16px;">
pip install webengage-migration
</pre>

---

## Usage

To initiate the migration process run the below command:

<pre style="font-size: 16px;">
we --migrate {users/events} -f "{filename.csv}" -d {datacenter} -lc {license_code}
</pre>

<br>

| Argument           | Description                                           | Type                |
|--------------------|-------------------------------------------------------|------------------------------------|
| `{users/events}`   | Type of data you're migrating (`users` or `events`)  | ⚠️ Required                        |
| `-f "filename.csv"`| Path to the input CSV file                           | ⚠️ Required                        |
| `-d {datacenter}`  | WebEngage datacenter (`in`, `ksa`, default is `us`)        | ⚙️ Optional  |
| `-lc {license_code}`| Your WebEngage license code                         | ⚠️ Required                        |

<br>

**Example:**


**Send users**: `we --migrate users -f "datafile.csv" -d in -lc in~~1234c456`

**Send events**: `we --migrate events -f "datafile.csv" -d in -lc in~~1234c456`

<br>

Once migration is initiated, provide the **API key for authorization**, **API key** will be found in **webengage dashboard for provided license code** under:

***Data Platforms → Integrations → Rest API → `API KEY`*** 

![Usage Example](https://logextractor.s3.ap-south-1.amazonaws.com/apikey.png)

---


## WebEngage API Rate Limits

WebEngage limits bulk event / users API usage to:

- **25 events / users** per API request  
- **500 requests** per minute (Total **12,500 events** per minute)

This tool automatically respects the above limits by batching and throttling requests.

---

## Legal Notice

This tool is an **internal property** of **WebEngage** and is strictly for **migration purposes**. It is owned by **Nipun Patel (Copyright)** and any misuse, unauthorized distribution, or external sharing will lead to **legal consequences**.

---

© WebEngage. All rights reserved.