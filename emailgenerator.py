import yagmail
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time
import os


def main():
    return setupGspread()


def setupGspread():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    matches_sheet = client.open("Berkeley_Grocery_Database").worksheet("Matches")  # Open the spreadsheet
    matchesRecords = matches_sheet.get_all_records()  # Get a list of all record

    return matchesRecords


def sendEmails(records):

    #html text of body, plz help format i cannot html
    content = """\
    <html><body><p>Hi {VolunteerName}!
    Thank you so much for signing up to volunteer to deliver groceries for seniors. You have been matched with the following person, who has requested to have groceries delivered:

    <strong>Name: </strong>{RequestName}
    <strong>Preference of contact: </strong>{PreferenceofContact}
    {Phone}
    <strong>Email: </strong>{Email}   

    They have requested that groceries be delivered at: around <strong>{Time}</strong> on <strong>{Day}</strong> from <strong>{Store}</strong>.
    
    {AlternateClause}
    
    Please follow <strong>Part 1</strong> and <strong>Part 2</strong> on this guideline document.

    <strong>Part 1: Communicate with the senior </strong>
    <ol><li>Copy-and-paste and send the following <span style="color: #0000ff;">blue text</span> to the senior(s) you are matched with through their preferred method of contact:</li>
    <blockquote><span style="color: #0000ff;"
    Hi! I am {VolunteerName}, and I am the volunteer paired with you to help you deliver your groceries. 
    <ol><li>What groceries would you like to order? Include quantity. If necessary, include the brand of the grocery item. If I cannot find the exact item, I will try to buy a close substitute based on my best judgment.</li>
    <li>You mentioned that you would like your groceries delivered at around {Time} on {Day} from {Store}. Are there any changes to this? I will try my best to get your groceries by that time.</li>
    <li>Where do you want the groceries placed? </li>
    <li>How are you going to pay for the grocery items? (PayPal/Venmo/WeChat Pay/Other) What is your username for that payment option? We do not accept cash to avoid necessary contact or transmission of disease.</li></ol>
    Thank you. Feel free to contact me if you have any further questions.
    </span></blockquote>
    <li>Make sure they give you all the necessary information you need in order to make a purchase.</li>
    <li>Make sure you agree upon a payment option with the senior before the purchase and decide with them whether you want them to pay before or after the delivery.</li></ol>

    <strong>Part 2: Deliver </strong>
    <ol><li> Please read and follow the following shopping <a href = "https://www.washingtonpost.com/news/voraciously/wp/2020/03/19/grocery-shopping-during-the-coronavirus-wash-your-hands-keep-your-distance-and-limit-trips/">guidelines</a> before you go shopping:
    <ol><li>Maintain at least 6 feet away from all other shoppers/people</li>
    <li>Wash your hands before and after you shop, 20 seconds at least</li>
    <li>Avoid touching your eyes, nose, and mouth</li>
    <li>Use hand sanitizer that contains at least 60% alcohol</li>
    <li>Touch as little as you shop</li>
    <li>Wear Gloves and Facemasks when possible</li></ol></li>
    <li>When delivering the food, please observe CDC guidelines (see <a href = "https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html">here</a>) and maintain 6 feet away from the senior you are delivering food to. 
    <ol><li>Please wipe down the handles of the grocery bags with disinfectant wipes if possible.</li>
    <li>Set the food down in the place they request and call/text them when their food has been delivered.</li>
    <li>Please do not see/speak to them in person. Call/text if necessary.</li>
    </ol></li></ol>
    Again, thank you so much for volunteering for this service--your effort is really appreciated! </p></body></html>
    """

    #runs through the records and customizes the body of the email according to it
    for info in records:
        format_string = {
                'VolunteerName': info['Volunteer Match'],
                'RequestName': info['Requester Name'],
                'PreferenceofContact': info['Contact'],
                'Phone': "{}".format("" if info['Contact'] == 'Email' else "<strong>Phone: </strong>" + str(info['Phone'])),
                'Email': info['Email'],
                'Time': "{}".format(str(24 - int(24*float(info['Time']))) + ' PM' if int(24*float(info['Time'])) > 12 else str(int(24*float(info['Time']))) + ' AM'),
                'Day': info['Day'],
                'Store': info['Store'],
                'AlternateClause': "{}".format("In case you cannot make it, please contact: \n\n<strong>Name: </strong>" + info['Alternate1'] + "\n<strong>Email: </strong>" + info['Email1'] + "\n<strong>Phone: </strong>" + str(info['Phone1']) + "{}".format("\n<strong>OR</strong> \n<strong>Name: </strong>" + info['Alternate2'] + "\n<strong>Email: </strong>" + info['Email2'] + "\n<strong>Phone: </strong>" + str(info['Phone2']) if info['Alternate2'] != '' else '\n***') if info['Alternate1'] != '' else '***')
                }

        receiver = "vishruti721@gmail.com" #we can change this to info['Match Email'] later
        ccer = "vishruti721@gmail.com"
        body = content.format(**format_string)
        yag = yagmail.SMTP("az9.yay@gmail.com")
        yag.send(
            to=receiver,
            cc=ccer,
            subject="Your Grocery Match",
            contents=body,)



#sends all the emails
sendEmails(main())

