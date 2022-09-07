class Gallery():

    def __init__(
        self, 
        the_class,
        the_query: list[dict]=None
    ):
        self.the_class=the_class
        self.the_query=the_query
        self.pos=0
        self.size=len(the_query)


    def next(self):
        if self.pos<self.size-1:
            self.pos+=1
        
        return self

    def back(self):
        if self.pos>0:
            self.pos-=1
        
        return self

    def show(self) -> str:
        return self.the_class(self.the_query[self.pos]).showToGallery()