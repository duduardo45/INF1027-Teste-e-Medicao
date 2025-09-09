package app_musica;

import java.util.ArrayList;
import java.util.List;

public class Usuario {
    String login;
    String senha;
    List<Playlist> playlists;
    List<Musica> favoritos;
    Musica escutando;


    public Usuario(String login, String senha) {
        this.login = login;
        this.senha = senha;
        this.playlists = new ArrayList<>();
        this.favoritos = new ArrayList<>();
    }

    public boolean verificarLogin(String nome, String senha) {
        if ((nome == this.login) && (senha == this.senha)) {
            return true;
        }
        return false;
    }

    public boolean favoritar(Musica m) {
        favoritos.add(m);
        return true;
    }
    public boolean escutar(Musica m) {
        escutando = m;
        return true;
    }
    public boolean criarPlaylist() {
        Playlist p = new Playlist();
        playlists.add(p);
        return true;
    }
}
