package app_musica;

import java.util.ArrayList;
import java.util.List;

public class Musica {
    String nome;
    List<Avaliacao> avaliacoes;

    public Musica(String nome) {
        this.nome = nome;
        this.avaliacoes = new ArrayList<>();
    }

    public String getNome() {
        return nome;
    }

    public Avaliacao getAvaliacaoUsuario(Usuario u) {
        Avaliacao avaliacao = null;
        for (Avaliacao a: avaliacoes) {
            if (a.getRevisor() == u) {
                avaliacao = a;
            }
        }
        if (avaliacao == null) {
            return null; 
            // poderia só retornar avaliação mas prefiro 
            // ter o tratamento do vazio explícito.
        }
        return avaliacao;
    }
    
    public float calcularMedia() {
        float soma = 0;
        for (int i = 0; i < avaliacoes.size() ; i++) {
            soma += avaliacoes.get(i).getEstrelas();
        }
        return soma/avaliacoes.size();
    }

    public boolean avaliar(Usuario user, int estrelas) {
        avaliacoes.add(new Avaliacao(estrelas,user));
        return true;
    }
}
