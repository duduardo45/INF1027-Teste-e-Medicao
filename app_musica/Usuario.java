package app_musica;

import java.util.List;

public class Usuario {
    String login;
    String senha;
    List<Playlist> playlists;
    List<Musica> favoritos;
    Musica escutando;

    public boolean verificarLogin(String nome, String senha) {
        if ((nome == this.login) && (senha == this.senha)) {
            return true;
        }
        return false;
    }

    public boolean favoritar() {
        return true;
    }
    public boolean escutar() {
        return true;
    }
    public boolean criarPlaylist() {
        return true;
    }
}
