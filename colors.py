class Colors:
    # NO PIECE
    no_piece = (0, 0, 0)

    # GAME OVER PIECE
    game_over_piece = (99, 99, 99)

    # TETROMINO
    i_piece = (13, 156, 215)
    j_piece = (33, 66, 199)
    l_piece = (227, 91, 3)
    o_piece = (227, 158, 2)
    s_piece = (89, 178, 2)
    t_piece = (175, 41, 138)
    z_piece = (215, 15, 54)

    # SILHOUETTE
    i_silhouette = (7, 77, 107)
    j_silhouette = (16, 32, 99)
    l_silhouette = (113, 45, 1)
    o_silhoeutte = (113, 79, 1)
    s_silhouette = (44, 88, 0)
    t_silhouette = (87, 20, 69)
    z_silhouette = (107, 7, 27)

    @classmethod
    def get_colors(cls) -> list:    
        return [cls.no_piece,
                cls.i_piece, cls.j_piece, cls.l_piece, cls.o_piece, cls.s_piece, cls.t_piece, cls.z_piece,
                cls.i_silhouette, cls.j_silhouette, cls.l_silhouette, cls.o_silhoeutte, cls.s_silhouette, cls.t_silhouette, cls.z_silhouette,
                cls.game_over_piece]