class Rules:
    def updateRule(newTitle, newDescription):
        if newTitle != Empty or newDescription != Empty:
            self.Title = newTitle
            self.Description = newDescription
    def LoadAllRules():
        rules = ["Rule 1: Read the manual before playing", "Rule 2: Each player starts on his own corner"]
        return rules