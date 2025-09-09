package app_musica;

import java.util.ArrayList;
import java.util.List;

public class Album {
    String titulo;
    int anoLancamento;
    List<Musica> musicas;

    public Album(String titulo, int anoLancamento) {
        this.titulo = titulo;
        this.anoLancamento = anoLancamento;
        this.musicas = new ArrayList<>();
    }

    public int getAnoLancamento() {
        return anoLancamento;
    }

    public String getTitulo() {
        return titulo;
    }

    public List<Musica> getMusicas() {
        return musicas;
    }

    public int getQtdeMusicas() {
        int res = 0;
        for (Musica musica : musicas) {
            res++;
        }
        return res;
    }
}
