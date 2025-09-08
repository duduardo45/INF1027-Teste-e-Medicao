package app_musica;

import java.sql.Date;
import java.util.List;

public class Artista {
        String nomeArtistico;
        String nomeReal;
        Date dataNascimento;
        List<Album> albuns;
        List<Musica> solos;

    public String getNomeArtistico() {
        return nomeArtistico;
    }

    public String getNomeReal() {
        return nomeReal;
    }

    public Date getDataNascimento() {
        return dataNascimento;
    }

    public int getQtdeAlbum() {
        return 0;
    }

    public int getQtdeMusicas() {
        return 0;
    }
}
