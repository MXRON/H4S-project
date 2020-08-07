# H4S-project
The project is a database that stores your 'content' (Username, Password, Date uploaded) for different websites. It has many functions including 1. Creating content 2. Updating content 3. Deleting content 4. Reading content

Every time content is created the option of generating a random password with any desired length is presented in order to provide more protection against cybe threats. The password consists of a random proportion of letter, numbers and symbols. The letters, numbers, and symbols are of course also random.

The functions interact with each other a lot, which I find interesting. 
Everytime the 'update' or 'delete' functions are called, the 'reading_content' function is used to check if the content is present for the picked website and this content is displayed.
Everytime the 'reading content' function finds that the inputted website does not exist, it triggers the 'create content' function if the user wants to create the content for this website.
So if you choose to try update/delete non-existant content, then realise it doesn't exist and choose to create content for this website, 3 functions will be used (update/delete, read, create)!

Almost all of the time there are while loops, so if the user inputs wrong, the question/commands will be reprinted.

