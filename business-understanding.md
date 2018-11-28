## Business Understanding


### Identifying your business goals


#### Background

Music is everywhere - there is usually some playlist playing in the background at larger public locations like shopping centres or there is a radio playing elsewhere (car, workplace, home). However it is not uncommon to privately enjoy music through various medium. As the time has moved forward, the means to listen music and the variety of music have expanded and become more accessible.

This has introduced however a new kind of challenge to services that offer "unlimited access" to their music library, such as Spotify: how to find new music that listeners would like? (New as in different, not necessarily recent.) From a business standpoint this would lead to emotionally satisfied customers that would stay subscribed to the service.

It is quite typical to assume that songs by the same artist or from the same genre would likely suit the same listener. However in a survey carried out in 2008, people confessed that lyrics of a song do play an important role in better understanding and appreciating it ([source](https://www.telegraph.co.uk/news/uknews/2483433/Elvis-Presleys-Cant-Help-Falling-In-Love-is-favourite-love-song.html)).


#### Business goals

Although this project is not intended to benefit any single business nor has business-oriented goals, we are seeking into ways of measuring song performance on lyrics alone in order to provide relevant recommendations and find commonly occuring themes in songs. The ultimate goal is to compile a playlist of songs that would resemble something that is similar to a top 100 chart.

At least initially the benefit will be for ourselves to discover new old music in an interesting way, if the method subjectively works, it could benefit anyone that listens music when certain adjustable parameters are introduced - songs that they like or don't like and a wider collection of song lyrics. Same idea could be used by businesses that already deliver music, by using pre-existing list of liked songs and extensive music libraries.


#### Business success criteria

Since there are as many different tastes of music as there are people, it is objectively difficult to assess whether the top songs that have been picked would actually perform well without polling a wide range of potential audience. 

Both team members will independently evaluate songs that make it to the top playlist and give their own opinion. If the general outcome is positive, the project is considered a success from a business standpoint. Feedback from poster session will indicate whether the topic itself is something worth further research potentially leading up to a new kind of service.


### Assessing your situation


#### Inventory of resources



*   **Data** \
All data is obtained from datasets hosted in Kaggle, however the original sources of the data are from either lyrics hosting sites or Wikipedia. Some datasets do provide scripts that were used to scrape the data from the original sources, which will be useful if more recent data is needed or any additional criteria available will be required to scrape.
*   **Project members** \
Team consisting of two members - Indrek Ardel and Mateus Surrage Reis. At the time of writing outside help other than course instructors is not being considered.
*   **Prior research** \
There are several research papers that have already analyzed specifically song lyrics, which project members have read in past. The papers themselves will be referred to at a later date and used to make design decisions for scoring algorithm in order to make better use of time.
*   **Hardware** \
Team members will have to make do with the hardware at their disposal - personal desktop/laptop computers.
*   **Software** \
All tasks will be carried out in Python programming language whenever possible and only free libraries and frameworks will be considered. Most likely tools used will be similar to, if not the same, as the ones covered in the course (standard library, pandas, sklearn, etc...).


#### Requirements, assumptions, and constraints

The project has a hard deadline which is set by the course - Monday, Dec 17, at 18:00. However another deadline is set internally to avoid any unforeseen difficulties - apart from small tweaks, everything shall be done by the 15th.

The song lyrics are likely copyrighted, which could be an issue if work is produced commercially. The project will refrain from profiting monetarily in order to avoid any kind of wrongdoing.

As all the data is publicly available, there are no data security considerations.


#### Risks and contingencies

There is always a slight risk in terms of a project member being unable to complete work for a particular reason (illness, family events, etc). To mitigate this risk, tasks are set with a deadline that allows for a big enough buffer to re-do the work necessary by other team member.

Failures in terms of hardware, software and infrastructure are mitigated by using commonly available tools, which makes it possible to easily swap out any component in the process (by means of loaning a computer or using their internet connection temporarily).

One of the biggest risks lies within the choice of topic itself - it is possible that there is no fruitful outcome from the analysis, which would be obviously a failure in terms of the project. Prior research still suggests that some patterns exist, which makes this outcome less likely. However if it ever comes to this, a re-evaluation of the goals for the project will be required.


#### Terminology

Project members feel that nearly all fields in data are self-explanatory for anyone vaguely familiar with the concept of songs and music industry (song title, lyrics, release year, artist, song title, chart ranking).

As with data-mining terms, it feels slightly early to say which techniques specifically will be used, but course material will be relied on for any defined terms to avoid ambiguity. Any terms not covered will be defined during the process.


#### Costs and benefits

There are no noticeable costs that can be directly translated to money. Some costs are unavoidable (like electricity and internet connection), but these should not impact fulfilling goals of project in any way.

 \
As the work is done with no expectation of payment, time and effort put into the project will make up the biggest "cost" of the project. As far as the work does benefit is up to team member to decide working on the task and adjusting the schedule accordingly.


### Defining your data-mining goals


#### Data-mining goals

The goals will vaguely describe milestones of the project.

Before any work on data can begin, some augmenting of data and cleaning is required. The intention is to add year of release for all of the songs in order to gain better insight to trends within lyrics as the time is passing.

Once all song datasets contain data for all fields, duplicates will need to be removed.

For chart dataset, more recent charts than 2015 are also of interest. Access to scripts that were used to scrape the songs are of help here.

With data in desired format, development of a model to rank similarity of songs can begin, this will serve as the main deliverable that will make or break the project.

After a ranking algorithm is developed, an utility needs to be created which will produce a playlist for a music streaming service - likely YouTube or Spotify. This will make evaluating the songs more interactive and enjoyable experience.

Another model is attempted to classify the year when a song was written in order to identify subtle hints whether a song is old-fashioned.

The most important deliverable - project poster, which will serve as a presentation for the whole project which will highlight the findings from the process and other deliverables. There are likely some statistics or visualizations required in order to convey findings in a meaningful manner.


#### Data-mining success criteria

As with business goals, quantitative assessment could prove difficult. Which is why both team members will assess the model independently, potentially pointing out examples how the model model gets things right (eg similarities between the songs in chart and the ones suggested by model, whether there is a clear distinction how songs rank against eachother - are scores given apart far enough, etc...) and success will be determined whether the assessments are both positive and agree with eachother.
