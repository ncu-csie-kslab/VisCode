USE jupyterhub;

INSERT INTO system_announcements(type, title, content) VALUES ('system', '系統公告', '系統公告');
INSERT INTO system_announcements(type, title, content) VALUES ('normal', '公告', '一般公告');
INSERT INTO user_passwords(name, password) VALUES ('admin', 'kslab35356');