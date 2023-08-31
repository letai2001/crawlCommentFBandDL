"""
    AI se cu ri ty
"""
class Post:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.time_crawl = ""
        self.link = ""
        self.author = ""
        self.author_link = ""
        self.avatar = ""
        self.created_time = ""
        self.content = ""
        self.image_url = []
        self.like = 0
        self.comment = 0
        self.haha = 0
        self.wow = 0
        self.sad = 0
        self.love = 0
        self.angry = 0
        self.share = 0
        self.domain = ""
        self.hastag = []
        self.music = ""
        self.title = ""
        self.duration = 0
        self.view = 0
        self.description = ""
        self.video = []
        self.source_id = ""
        
    #Hàm xác định xem post được crawl đủ hay chưa
    def is_valid(self) -> bool:
        is_valid = self.id != "" and self.author != "" and self.link != "" and self.created_time 
        return is_valid

    def __str__(self) -> str:
        string = ""
        for attr_name, attr_value in self.__dict__.items():
            string =  f"{attr_name}={attr_value}\n" + string
        return string
    def to_dict_comment(self) -> dict:
        return {"id": self.id,
                "type": self.type,
                "time_crawl": self.time_crawl , 
                            "author":{ 'author_link': self.author_link ,  
                                    'auth_name': self.author
                                } 
                        ,"time":self.created_time ,
                        "content": self.content , 
                        "video_only": self.video , 
                        "image_post_list":   self.image_url ,
                    
                        "number_reaction": {"Like": self.like, "Love": self.love , 
                                     "Wow": self.wow , 
                                    "Haha": self.haha , "Angry": self.angry,
                                    "Huhu": self.sad,
                                   
                            },
                        "source_id": self.source_id , 
                         }
    def to_dict_post(self) -> dict:
        return      {"id": self.id, 
                     "self.type": self.type , 
                      "time_crawl": self.time_crawl , 
                     "self.created_time": self.created_time , 
                     
                            "author":{ 'author_link': self.author_link ,  
                                    'auth_name': self.author
                                } ,
                            "number_comment": self.comment 

                        ,"time":self.created_time , "content": self.content , 
                        "video_only": self.video , 
                        "image_post_list":   self.image_url ,
                    
                        "number_reaction": {"Like": self.like, "Love": self.love , 
                                     "Wow": self.wow , 
                                    "Haha": self.haha , "Angry": self.angry,
                                    "Huhu": self.sad, 
                        }
                        }
