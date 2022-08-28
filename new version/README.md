# Use the old version with onlinesim support please. 
# This Folder will be updated when i'm ready to upload a completly rewritten Version with a lot of new features.

### Adding your own Phone Service (Beginner Level)
------------------------------------
- To be able to add your own Service, you need to know what APIs are and how to use them in Python.
- I made the Code easy to understand with seperating things in different files.
- The Whole main.py file include specific ifstatements which are checking for the phone service used.
- This way you can use the same variable & function names & apply the same logic within this main.py file and the files inside the phoneservices folder
- Put it inside  elif and have more phone service support.
- Here a Example: if str(PHONESERVICE).lower() == "vaksms": NUMBER, TZID = vaksms.ordernumber()
- You can change the example to elif str(PHONESERVICE).lower() == "other service" and add your own logic.
- To fully implement a own service, you need to take a look to the already supported services in the phoneservices folder, copy the file & and the new API endpoints + import it to the main file in the same way like i did in the standard supported Services.
