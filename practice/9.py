class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song_name):
        self.songs.append(song_name)
        return f"Successfully added {song_name}"
    
    def delete_song(self, song_name):
        if song_name in self.songs:
            self.songs.remove(song_name)
            return "SUCCESSFULLY DELETED"
        else:
            print("FAILED TO FIND THE SONG")



p1 = Playlist("Water Later")
print(f"Before: {p1.songs}")

p1.add_song("Faasle")
p1.add_song("Tere Bin")
p1.add_song("Anshu")
p1.add_song("SDSFLH")



print(f"After: {p1.songs}")

p1.delete_song("FAASLE")

print(f"After DELETING: {p1.songs}")

    