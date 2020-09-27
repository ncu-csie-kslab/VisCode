FROM jupyter/scipy-notebook:74b0a01aebb1

USER root

COPY  . /root/viscode-extension/

USER root
RUN sudo -H /opt/conda/bin/pip install /root/viscode-extension/. && \
    jupyter nbextension install --py viscode --sys-prefix --system && \
    jupyter nbextension enable --py viscode --sys-prefix --system && \
    jupyter serverextension enable --py viscode --sys-prefix --system

USER $NB_UID