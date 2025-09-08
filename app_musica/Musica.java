package app_musica;

import java.util.List;

public class Musica {
    String nome;
    List<Avaliacao> avaliacoes;
    
    public float calcularMedia() {
        float soma = 0;
        for (int i = 0; i < avaliacoes.size() ; i++) {
            soma += avaliacoes.get(i).getEstrelas();
        }
        return soma/avaliacoes.size();
    }

    public void avaliar(Usuario user, int estrelas) {
        avaliacoes.add(new Avaliacao(estrelas,user));
    }
}
