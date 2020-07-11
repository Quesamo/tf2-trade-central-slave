from discord.ext import tasks, commands

import requests
import json
import datetime




class unupc(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command() #the main unupc command
    async def unupc(self, ctx, item_input): #defines the command itself
        
        def getPrices(): #gets the saved API response and formats it for unusual price checking. returns a list of possible unusual items if successful, returns None if not
            with open('commands/call_APIs/api_responses/backpacktf_igetpricesv4_response.json', 'r') as sampleresponse:
                response = json.load(sampleresponse)
            
            if response['response']['success'] == 0: #if the request was unsuccessful
                return None #doesn't need to send a message to say the request was unsuccessful, because the API will be called automatically every 2 hours
            else: #if the request was successful
                unusual_item_list = [] #adds every item that be unusual to a list
                for item in response['response']['items']: #iterates through every single item
                    for quality in response['response']['items'][item]['prices'].keys(): #iterates through every possible quality of the item
                        if quality == '5': #if the item has can have the unusual quality (5)
                            unusual_item_list.append(item) #adds the item to the list of items that can be unusual
                
                unusual_item_list.sort() #sorts the list of items that can be unusual, alphabetically. helps make the command more predictable in cases where several hats start with the given hat name
                return unusual_item_list, response #returns both the list of items that can be unusual (for the hat finding), and the full response (for pricing), as a tuple

        if '.' not in ctx.message.content: #if the message doesn't contain a period
            await ctx.send("Invalid command syntax: correct syntax is ``effect.hat``")
            return

        item_input = item_input.split('.') #splits the params of the command at a period (correct syntax is effect.hat), to create a list with 2 entries
        print(item_input) #for debugging

        getPrices_result = getPrices() #needs to be assigned like this to avoid calling the function several times
        unusual_item_list = getPrices_result[0] #the list of items that can be unusual
        response = getPrices_result[1] #the full response from the API

        if unusual_item_list == None:
            await ctx.send("Couldn't call backpack.tf's API, something has gone mighty wrong")
            return #leaves the function if it can't call the api



        #hat autocomplete
        item_hat = None
        for item in unusual_item_list: #cycles through the list of items that can be unusual
            if item_input[1].lower() in item.lower(): #if the hat string is in the name of the item
                item_hat = item #sets the item_hat (base item of the hat/taunt/whatever in question) to the matching entry
                break
        
        if item_hat == None: #if a matching hat name isn't found, the var remains as None
            await ctx.send("Couldn't find a hat with that name. Make sure you're using correct syntax (``effect.hat``)")
            return #leaves the function



        #effect autocomplete
        item_effect = None 
        effects_dict = {"Nebula":"99","Burning Flames":"13","Spellbound":"74","It's A Secret To Everybody":"46","Scorching Flames":"14","Harvest Moon":"45","Arcana":"73","Abduction":"91","Sunbeams":"17","Darkblaze":"79","Bonzo The All-Gnawing":"81","Poisoned Shadows":"76","Knifestorm":"43","Stormy 13th Hour":"47","Hellfire":"78","Cloudy Moon":"38","Energy Orb":"704","Misty Skull":"44","Anti-Freeze":"69","Chiroptera Venenata":"75","Roboactive":"72","Demonflame":"80","Atomic":"92","Something Burning This Way Comes":"77","Galactic Codex":"97","Voltaic Hat Protector":"96","Purple Energy":"10","Death by Disco":"100","Green Energy":"9","Ether Trail":"103","Frostbite":"87","Subatomic":"93","Death at Dusk":"90","Ancient Codex":"98","Time Warp":"70","Cool":"703","Morning Glory":"89","Green Black Hole":"71","Amaranthine":"82","Magnetic Hat Protector":"95","Ghastly Ghosts Jr":"85","The Ooze":"84","Haunted Phantasm Jr":"86","Circling Heart":"19","Sulphurous":"64","Electric Hat Protector":"94","Eldritch Flame":"106","Cauldron Bubbles":"39","Stare From Beyond":"83","Haunted Ghosts":"8","Nether Trail":"104","It's a mystery to everyone":"101","Phosphorous":"63","Ancient Eldritch":"105","Flaming Lantern":"37","Hot":"701","Isotope":"702","It's a puzzle to me":"102","Vivid Plasma":"16","Molten Mallard":"88","Tesla Coil":"108","Eerie Orbiting Fire":"40","Haunted Phantasm":"3011","Searing Plasma":"15","Disco Beat Down":"62","Ghastly Ghosts":"3012","Starstorm Insomnia":"109","Starstorm Slumber":"110","Power Surge":"68","Circling Peace Sign":"18","Cloud 9":"58","Electrostatic":"67","Neutron Star":"107","Blizzardy Storm":"30","Circling TF Logo":"11","Infernal Flames":"3015","Infernal Smoke":"3016","Purple Confetti":"7","Stormy Storm":"29","Spectral Swirl":"3014","Holy Grail":"3003","Screaming Tiger":"3006","Miami Nights":"61","Green Confetti":"6","Fountain of Delight":"3005","Memory Leak":"65","Hellish Inferno":"3013","Showstopper":"3001","Terror-Watt":"57","Orbiting Fire":"33","Overclocked":"66","Kill-a-Watt":"56","Massed Flies":"12","Smoking":"35","Bubbling":"34","Steaming":"36","Orbiting Planets":"32","Dead Presidents":"60","Nuts n' Bolts":"31","'72":"3004","Aces High":"59","Skill Gotten Gains":"3007","Mega Strike":"3010","Silver Cyclone":"3009","Midnight Whirlwind":"3008"}
        #some exceptions (effects that won't work on their own when entered)

        if item_input[0].lower() == 'orbiting fire': #item_effect will otherwise be set to Eerie orbiting fire, even when using the full name
            item_effect = 'Orbiting Fire'
        else:
            #print(item_input[0]) #for debugging
            for effect in effects_dict.keys(): #cycles through every effect in the dict
                #print(effect) #for debugging
                if item_input[0].lower() in effect.lower(): #if the key name matches the given effect name
                    item_effect = effect #sets the given item's effect to the current one
        
        if item_effect == None: #if the specified effect couldn't be found in the dict
            await ctx.send("Couldn't find an effect with that name. Make sure you're using correct syntax (``effect.hat``)")
            return #quits the function

        print(f"$unupc used for item {item_effect, item_hat}") #for... wait for it... debugging
        #print(effects_dict[item_effect]) #guess

        try:
            price_currency = response['response']['items'][item_hat]['prices']['5']['Tradable']['Craftable'][effects_dict[item_effect]]['currency']
            price_low     =  response['response']['items'][item_hat]['prices']['5']['Tradable']['Craftable'][effects_dict[item_effect]]['value']
            
            try: #if the item has a high value, uses that to create an average
                price_high   =   response['response']['items'][item_hat]['prices']['5']['Tradable']['Craftable'][effects_dict[item_effect]]['value_high']
                price_average = (price_low + price_high)/2 #calculates the price average off the low and high values
                if '.' in str(price_average) and str(price_average)[-1] == '0': #if the average price has a comma in it, but ends in a 0, converts it to int to remove the unnecessary decimal
                    price_average = int(price_average)

                price_message = f"The {item_effect} {item_hat} is priced at {price_low}-{price_high} {price_currency} ({price_average})"
            
            except KeyError: #if the item does not have a high value, uses a different format for the output message
                price_message = f"The {item_effect} {item_hat} is priced at {price_low} {price_currency}" 
                
        except KeyError: #if a hat with the specified effect can't be found
            await ctx.send(f"An error occured: The {item_effect} {item_hat} is either unpriced, or doesn't exist")
            return

        await ctx.send(price_message)


    





    
#consider making things more object based















def setup(bot): #runs when the extension is loaded
    
    bot.add_cog(unupc(bot))
    print("Cog unupc loaded!")