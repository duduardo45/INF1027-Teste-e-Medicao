package app_musica;

public class Avaliacao {
    int estrelas;
    Usuario revisor;

    public Avaliacao(int estrelas, Usuario revisor) {
        this.estrelas = estrelas;
        this.revisor = revisor;
    }

    public int getEstrelas() {
        return estrelas;
    }
    public Usuario getRevisor() {
        return revisor;
    }
}
