[A small write-up here.](https://medium.com/@nhf/whats-up-with-all-of-those-identical-comments-on-the-fcc-net-neutrality-docket-105835f59c3e)

# What is this repo?

Lately, there has been controversy surrounding the FCC's net neutrality actions. The FCC has opened up a docket for public comment: 17-108, "Restoring Internet Freedom". Many astute journalists and observers have noticed a ton of identical comments being filed through the FCC's comment system. These comments all contain the exact same phrasing:

> The unprecedented regulatory power the Obama Administration imposed on the internet is smothering innovation, damaging the American economy and obstructing job creation. I urge the Federal Communications Commission to end the bureaucratic regulatory overreach of the internet known as Title II and restore the bipartisan light-touch regulatory consensus that enabled the internet to flourish for more than 20 years. The plan currently under consideration at the FCC to repeal Obama's Title II power grab is a positive step forward and will help to promote a truly free and open internet for everyone.

This repository contains all of those comments in JSON format (in the zip file), along with summary data in the CSV. The data is from the FCC's electronic comment filing system. 

The data is public record:

> "...under the rules of the Commission, public comments on rulemakings are routinely available to the public--unless confidentiality is requested (47 CFR 0.459)--via either the Commission's electronic comment filing system (ECFS) at http://www.fcc.gov/cgb/ecfs/ or the public Reference Information Center (RIC) at http://www.fcc.gov/cgb/ric.html"

# About the data
Everything should be pretty self explanatory. 

* Everything is zipped because it's large.

* JSON files are the raw JSON records from the FCC's API.

* CSV files are summary data that I used to produce visualizations.

* Field names are obvious, except for the "suspicious" field -- this is one that I added, which is binary (1 if the hash of the text matches the hash of the spammy message, 0 otherwise).

* May 11th is spammy comments only. May 15th is all extant comments.

# Getting the data
The data was gathered using the filing system's [public API](https://www.fcc.gov/ecfs/public-api-docs.html). The API requires a key from [data.gov](http://data.gov)

As of May 10th, 2017 at 9:56PM EST, there were 128946 comments gathered.

As of May 15th, 2017 at 6:00PM EST, there were 1584181 comments gathered (this is all of them).

# Oops
I had to nuke the repository and recreate it because I messed up with GitHub's large file storage system.

PowerBI version was merged by [Huntleychris](https://github.com/huntleychris). Sorry Chris, your merge history was lost. 
