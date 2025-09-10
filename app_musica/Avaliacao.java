package app_musica;

public class Avaliacao {
    int estrelas;
    Usuario revisor;
    Musica musica;

    public Avaliacao(int estrelas, Usuario revisor, Musica musica) {
        this.estrelas = estrelas;
        this.revisor = revisor;
        this.musica = musica;
    }

    public int getEstrelas() {
        return estrelas;
    }
    public Usuario getRevisor() {
        return revisor;
    }
}
