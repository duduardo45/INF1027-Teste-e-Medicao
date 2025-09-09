package app_musica;

import java.util.ArrayList;
import java.util.List;

public class Playlist {
    List<Musica> musicas;

    public Playlist() {
        this.musicas = new ArrayList<>();
    }
    
    public boolean adicionarMusica(Musica m) {
        musicas.add(m);
        return true;
    }
}
