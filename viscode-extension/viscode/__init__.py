import os

def _jupyter_server_extension_paths():
    paths = [
        {
            "module": "viscode.server_extension.nb_coding_logger"
        },{
            "module": "viscode.server_extension.tree_logger"
        },{
            "module": "viscode.server_extension.nb_logger"
        },{
            "module": "viscode.server_extension.user_access_roles"
        },{
            "module": "viscode.server_extension.tree_announcement"
        },
        {
            "module": "viscode.server_extension.users"
        },
    ]
    return paths


def _jupyter_nbextension_paths():
    paths = [
        dict(
            section="tree",
            src=os.path.join('nbextension', 'tree_announcement'),
            dest="tree_announcement",
            require="tree_announcement/main"
        ),
        dict(
            section="tree",
            src=os.path.join('nbextension', 'toolbar'),
            dest="toolbar",
            require="toolbar/main"
        ),
        dict(
            section="notebook",
            src=os.path.join('nbextension', 'nb_coding_logger'),
            dest="nb_coding_logger",
            require="nb_coding_logger/main"
        ),
        dict(
            section="tree",
            src=os.path.join('nbextension', 'tree_logger'),
            dest="tree_logger",
            require="tree_logger/main"
        ),
        dict(
            section="notebook",
            src=os.path.join('nbextension', 'nb_logger'),
            dest="nb_logger",
            require="nb_logger/main"
        ),
        # dict(
        #     section="notebook",
        #     # the path is relative to the `my_fancy_module` directory
        #     src="static",
        #     # directory in the `nbextension/` namespace
        #     dest="mypluging",
        #     # _also_ in the `nbextension/` namespace
        #     require="nbgit/cell_result_detect")
    ]
    return paths


# def load_jupyter_server_extension(nbapp):
#     setup_handlers(nbapp)
