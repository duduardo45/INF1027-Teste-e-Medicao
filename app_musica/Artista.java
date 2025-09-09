package app_musica;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;

public class Artista {
    String nomeArtistico;
    String nomeReal;
    Date dataNascimento;
    List<Album> albuns;
    List<Musica> solos;

    public Artista(String nomeArtistico, String nomeReal, Date dataNasc) {
        this.nomeArtistico = nomeArtistico;
        this.nomeReal = nomeReal;
        this.dataNascimento = dataNasc;
        this.albuns = new ArrayList<>();
        this.solos = new ArrayList<>();
    }

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
        int res = 0;
        for (Album album : albuns) {
            res++;
        }
        return res;
    }

    public List<Album> getAlbuns() {
        return albuns;
    }

    public List<Musica> getSolos() {
        return solos;
    }

    public int getQtdeMusicas() {
        int res = 0;
        for (Musica musica : solos) {
            res++;
        }
        for (Album album : albuns) {
            res += album.getQtdeMusicas();
        }
        return res;
    }
}
