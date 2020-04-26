# hack:now submission

## Just a Google Form?

**We provide two google forms for the volunteers and seniors to fill out based on preferences of grocery store, delivery day and time, and location.** Why a Google Form? Because we’re focused on **ease of access**—because seniors aren’t as technologically literate, a Google Form is the best way to keep things simple. The complexities are handled in the back-end, by us. 


Using the google sheets API, we loaded and saved the Google Form results directly through Python. We then put users into “buckets” based and classified each user based on their availability. 

In order to guarantee that a maximum number of seniors get a volunteer match with their preferences, and each volunteer is provided exactly one senior match, we coded a satisfiability solver—modeled after the well-known “Boolean Satisfiability Problem”—which recursively determines the best set of matches, prioritizing senior citizens along the way. 

## An Android App

In order to make our resource as accessible as possible, we have also built an Android app that encapsulates the aforementioned forms, and more.

The app not only gives seniors and volunteers easy access to the forms mentioned earlier but also provides Berkeley residents with real-time, localized updates of the Corona Virus situation through the Postman API. 


Additionally, users can access our self-curated, detailed listings of senior, youth, and grocery resources—all localized specifically to Berkeley. These resources help contribute to our end goal: **to provide the city of Berkeley with an all-purpose Covid-19 Assistant**

## A Lesson From a Computer

During this hackathon, we also trained several machine learning models with COVID-19 data from Alameda County and California. We spent a considerable portion of our time experimenting with Machine Learning—a seemingly unrelated aspect of our application—to get a better grasp of the situation we are dealing with. Using models such as the Decision Tree Model, the Ridge Regression Model, and the Boosted Trees Model to better understand the data, we were able to better conceptualize the exponentially growing threat that is Covid-19. As such, this inspired us to work passionately and diligently on our project during the 36 hours allotted. 


## Now What
It all started as a Google Form. It then adapted to a complex matching algorithm modeled around the Boolean Satisfiability Problem. Then, it morphed into a platform with live updates and localized resources. And now, it’s an Android app too. The question is, **now what?**

As I type this description, at 3:43 AM—I feel a sense of aspiration overtaking me. I’m thinking to myself, “If we did all that in 36 hours, imagine what we can do in 36 days. In 36 weeks. In 36 months?” The project doesn’t end here. After creating the ultimate resource for the city of Berkeley, we plan to expand to other cities as well. Our goal is to stay localized and relevant whilst helping as many people as possible. These two things are not mutually exclusive, and with the help of some mentorship—that we hopefully gain through this hackathon—we know we can make it work. 

