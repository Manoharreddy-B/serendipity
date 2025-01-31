class User:
    def __init__(self):
        
        self.name = ''
        self.email = ''
        self.dob = ''
        self.phoneno = ''
         
    def update(self, name, email, dob, phoneno):
        self.name = name
        self.email = email
        self.dob = dob
        self.phoneno = phoneno
        
    def getUser(self):
        dic = {'name':self.name,
            'email':self.email,
            'dob':self.dob,
            'phoneno':self.phoneno}
        return dic
    

    