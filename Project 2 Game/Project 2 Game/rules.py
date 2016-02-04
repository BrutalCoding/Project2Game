class Rules:
    def updateRule(newTitle, newDescription):
        if newTitle != Empty or newDescription != Empty:
            self.Title = newTitle
            self.Description = newDescription
    def LoadAllRules():
        rules = ["1. The one that throws the highest amount with the dice will start the game.",
                 "2. Every player has his own corner (size of 3 boxes) and starts from that corner.The game is played clockwise.",
                 "3. Every player starts with 100 Levenspunten(lifepoints) written on the notepad and15 (physical) conditionpoints.",
                 "4. Every player has a score card of a character with matching pawn(boxing glove).",
                 "5. You throw the dice to move forward on the boardgame.",
                 "6. When a player lands on the ‘Fight’ space, the player is obliged to fight a Super-fighter regardless ",
                 "    if there is a opponent on the same space. regardless if there is a opponent on the same space.",
                 "7. The Superfighter is specified by taking a Superfighter-card from the deck on the boardgame. After using ",
                 "    the Superfighter-card, you should put it back under the deck of cards.",
                 "8. Depending on the thrown amount of dice eyes you can choose an attack from the Scorekaart with the",
                 "    right amount of conditionpoints.",
                 "9. When one does not have any or not enough conditionpoints there can not be any damage done to the opponent!",
                 "10. When players have to fight and both do not have any or not enough condition- points the defender receives 15 damage.",
                 "11. The highest amount of damage - the lowest amount of damage = damage dealt to the player with the lowest",
                 "     amount of damage.",
                 "12. If 2 players meet at the same box, then the 2 players are obliged to fight with eachother. The player that lands ",
                 "     on the box last will be the attacker. More than 2 players in a box? The last player must choose an opponent.",
                 "13. When there is more than one player on the ‘Fight’ space there will only be a fight with",
                 "     the Superfighter and not with eachother",
                 "14. You receive 15 conditionpoints if you pass or land on your own corner(max = 15 conditionpoints).",
                 "15. You receive 10 Levenspunten if you land on your own corner(max = 100 Leven-spunten).",
                 "16. You can keep record of your Levenspunten with the help of the notepad.",
                 "17. Remove your pawn when you have no (0) Levenspunten(lifepoints) left. You have lost the game. You are K.O.",
                 ""] 
        return rules