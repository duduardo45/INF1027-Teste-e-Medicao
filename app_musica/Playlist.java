package app_musica;

import java.util.ArrayList;
import java.util.List;

public class Playlist {
    List<Musica> musicas;

    public Playlist() {
        this.musicas = new ArrayList<>();
    }

    public List<Musica> getMusicas() {
        return musicas;
    }
    
    public boolean adicionarMusica(Musica m) {
        musicas.add(m);
        return true;
    }

    public boolean removerMusica(Musica m) {
        for (Musica n : musicas) {
            if (m == n) {
                musicas.remove(n);
                return true;
            }
        }
        return false;
    }
}
