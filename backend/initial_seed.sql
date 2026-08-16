PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE playlist_users (
            playlist_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            PRIMARY KEY (playlist_id, user_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
INSERT INTO "playlist_users" VALUES('3208f373-d0f4-4271-bff6-16357fda0589','a4c82220-a7d9-4b47-9ecc-023d39363a8f');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','13b3423d-84e3-4c70-8812-84cca8ac567b');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','2956e27a-aa67-4e1c-bafb-15437ad37d43');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','d790be9d-6cf5-4975-b442-580503242362');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','05f12efd-bd86-4ee8-b557-febe3cce05a8');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','e08a8951-39f5-4694-b0bf-7b1f0e7c6e71');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','bbcfa206-4dc8-46f3-9618-911bc660c963');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','618d35d5-de73-4066-aaa3-e2f4f8589378');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','3c70b9e6-d45a-453d-9381-49a37139e131');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','be5771f5-a5b5-4161-a10e-4bd489701ca5');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','bf898c63-fd09-4d94-a7ed-a74e36861ca0');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','c289101e-4052-426d-8442-70942392e7f1');
INSERT INTO "playlist_users" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','1cfb0503-265e-424c-a912-a252058da58a');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','13b3423d-84e3-4c70-8812-84cca8ac567b');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','2956e27a-aa67-4e1c-bafb-15437ad37d43');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','d790be9d-6cf5-4975-b442-580503242362');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','05f12efd-bd86-4ee8-b557-febe3cce05a8');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','e08a8951-39f5-4694-b0bf-7b1f0e7c6e71');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','bbcfa206-4dc8-46f3-9618-911bc660c963');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','618d35d5-de73-4066-aaa3-e2f4f8589378');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','3c70b9e6-d45a-453d-9381-49a37139e131');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','be5771f5-a5b5-4161-a10e-4bd489701ca5');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','bf898c63-fd09-4d94-a7ed-a74e36861ca0');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','c289101e-4052-426d-8442-70942392e7f1');
INSERT INTO "playlist_users" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','1cfb0503-265e-424c-a912-a252058da58a');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','13b3423d-84e3-4c70-8812-84cca8ac567b');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','2956e27a-aa67-4e1c-bafb-15437ad37d43');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','d790be9d-6cf5-4975-b442-580503242362');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','05f12efd-bd86-4ee8-b557-febe3cce05a8');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','e08a8951-39f5-4694-b0bf-7b1f0e7c6e71');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','bbcfa206-4dc8-46f3-9618-911bc660c963');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','618d35d5-de73-4066-aaa3-e2f4f8589378');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','3c70b9e6-d45a-453d-9381-49a37139e131');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','be5771f5-a5b5-4161-a10e-4bd489701ca5');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','bf898c63-fd09-4d94-a7ed-a74e36861ca0');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','c289101e-4052-426d-8442-70942392e7f1');
INSERT INTO "playlist_users" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','1cfb0503-265e-424c-a912-a252058da58a');
INSERT INTO "playlist_users" VALUES('bc881bdb-77ba-4393-9d85-8a96767735f2','760ef44a-f400-40c2-941a-afe0a9b6fd48');
CREATE TABLE playlists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            youtube_id TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL
        );
INSERT INTO "playlists" VALUES('4bad44ad-39da-49e3-aa07-8ccde6945cc2','CULTURAS DEL MUNDO','PLAVoI2KYXjxs','d790be9d-6cf5-4975-b442-580503242362','2026-07-23T18:41:30.011816+00:00');
INSERT INTO "playlists" VALUES('db7569b7-7863-45f2-bea9-07d01eab5bf0','METAL BETA SEASON','PLEg8JhD1tnoY','d790be9d-6cf5-4975-b442-580503242362','2026-07-23T18:43:51.630066+00:00');
INSERT INTO "playlists" VALUES('68179ce1-adf3-4027-9a6b-ef15746d0282','TECHNO/ELECTRO BETA SEASON','PLIMtvA4koKMw','d790be9d-6cf5-4975-b442-580503242362','2026-07-23T19:19:10.125694+00:00');
CREATE TABLE songs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            playlist_id TEXT NOT NULL,
            original_url TEXT NOT NULL,
            source_platform TEXT DEFAULT 'youtube',
            artist TEXT,
            title TEXT,
            youtube_video_id TEXT,
            art_url TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
        );
INSERT INTO "songs" VALUES('7f974795-29fc-45dd-b302-52c160fdd4e0','a4c82220-a7d9-4b47-9ecc-023d39363a8f','3208f373-d0f4-4271-bff6-16357fda0589','https://youtube.com/watch?v=123','youtube','Artista Test','Canción Test',NULL,NULL,'2026-08-14T00:00:00Z');
INSERT INTO "songs" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','d790be9d-6cf5-4975-b442-580503242362','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=h31THl8shy4','youtube','Bad Omens','Dethrone (Official Music Video)','h31THl8shy4','https://img.youtube.com/vi/h31THl8shy4/hqdefault.jpg','2026-07-23T19:17:43.638465');
INSERT INTO "songs" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','d790be9d-6cf5-4975-b442-580503242362','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=bUZ3EhZEVZ0&list=PLIMtvA4koKMw&index=1','youtube','Desconocido','vleermuis','bUZ3EhZEVZ0','https://img.youtube.com/vi/bUZ3EhZEVZ0/hqdefault.jpg','2026-07-23T19:19:52.961866');
INSERT INTO "songs" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','d790be9d-6cf5-4975-b442-580503242362','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://www.youtube.com/watch?v=D24dn9eXTwA','youtube','PinkPantheress','Girl Like Me (Official Audio)','D24dn9eXTwA','https://img.youtube.com/vi/D24dn9eXTwA/hqdefault.jpg','2026-07-23T19:20:38.106499');
INSERT INTO "songs" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','bf898c63-fd09-4d94-a7ed-a74e36861ca0','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=RJX0JykhIkc','youtube','Desconocido','TELEGRAM (Lyric Video) | Shot by: @Jodeiine ','RJX0JykhIkc','https://img.youtube.com/vi/RJX0JykhIkc/hqdefault.jpg','2026-07-23T19:51:12.967991');
INSERT INTO "songs" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','bf898c63-fd09-4d94-a7ed-a74e36861ca0','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=X-C5ug_-u-8','youtube','Code Orange','Take Shape (feat. Billy Corgan) [OFFICIAL VIDEO]','X-C5ug_-u-8','https://img.youtube.com/vi/X-C5ug_-u-8/hqdefault.jpg','2026-07-23T19:54:27.636447');
INSERT INTO "songs" VALUES('ac8afbab-8b06-49a6-bb0d-80ca4995eb76','bbcfa206-4dc8-46f3-9618-911bc660c963','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=P3-xZgLHhJ0&list=RDP3-xZgLHhJ0&start_radio=1','youtube','Orbit Culture','"Strangler" (Official Music Video)','P3-xZgLHhJ0','https://img.youtube.com/vi/P3-xZgLHhJ0/hqdefault.jpg','2026-07-23T20:07:36.549937');
INSERT INTO "songs" VALUES('1e748911-6cdc-4452-9f5a-3a760c1b439b','bbcfa206-4dc8-46f3-9618-911bc660c963','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=J3xmBRPIPTo&list=RDJ3xmBRPIPTo&start_radio=1','youtube','GEA','ÁCIDA','J3xmBRPIPTo','https://img.youtube.com/vi/J3xmBRPIPTo/hqdefault.jpg','2026-07-23T20:12:01.220867');
INSERT INTO "songs" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://music.youtube.com/watch?v=qU9mHegkTc4','youtube','Desconocido','505','qU9mHegkTc4','https://img.youtube.com/vi/qU9mHegkTc4/hqdefault.jpg','2026-07-23T20:17:33.2653');
INSERT INTO "songs" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','bf898c63-fd09-4d94-a7ed-a74e36861ca0','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://www.youtube.com/watch?v=jyJU2136ym4','youtube','Oasis','D''You Know What I Mean? (Official HD Remastered Video)','jyJU2136ym4','https://img.youtube.com/vi/jyJU2136ym4/hqdefault.jpg','2026-07-23T20:24:49.528584');
INSERT INTO "songs" VALUES('e4b28f21-b12c-418d-a165-3215bdfcb2dc','3c70b9e6-d45a-453d-9381-49a37139e131','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://music.youtube.com/watch?v=2D-UTGXnTdc&si=wclm5JzYKWhR3fti','youtube','Desconocido','Yummy (Righteous Remix)','2D-UTGXnTdc','https://img.youtube.com/vi/2D-UTGXnTdc/hqdefault.jpg','2026-07-23T20:31:30.083959');
INSERT INTO "songs" VALUES('014af269-6ce8-4e89-9540-41e0f4cab733','3c70b9e6-d45a-453d-9381-49a37139e131','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://music.youtube.com/watch?v=PXiTSX50BrY&si=U3ISyskV82X3_Cxm','youtube','Desconocido','Idols and Anchors','PXiTSX50BrY','https://img.youtube.com/vi/PXiTSX50BrY/hqdefault.jpg','2026-07-23T20:36:08.635321');
INSERT INTO "songs" VALUES('b420d7be-7e1b-4fb9-a4b7-166db896f8ad','3c70b9e6-d45a-453d-9381-49a37139e131','68179ce1-adf3-4027-9a6b-ef15746d0282','https://music.youtube.com/watch?v=0XjNide61_Y&si=3n1vEQurmYnj63YG','youtube','Desconocido','RAPTURE','0XjNide61_Y','https://img.youtube.com/vi/0XjNide61_Y/hqdefault.jpg','2026-07-23T20:39:13.044396');
INSERT INTO "songs" VALUES('539dd2b9-88d9-4d82-a099-0b7a0460f0b1','c289101e-4052-426d-8442-70942392e7f1','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://www.youtube.com/watch?v=D7opDcDgTdM','youtube','FANTA ROSARIO','SI ME HICIERA EL DE LA LENGUA (VIDEO OFICIAL)','D7opDcDgTdM','https://img.youtube.com/vi/D7opDcDgTdM/hqdefault.jpg','2026-07-23T22:09:21.255339');
INSERT INTO "songs" VALUES('2ade6604-1b2c-4674-a3fc-d87bc8c1644f','c289101e-4052-426d-8442-70942392e7f1','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=l9VFg44H2z8','youtube','Five Finger Death Punch','Wash It All Away (Explicit)','l9VFg44H2z8','https://img.youtube.com/vi/l9VFg44H2z8/hqdefault.jpg','2026-07-23T22:11:19.466103');
INSERT INTO "songs" VALUES('f167a0f9-7ca4-41ff-bd0d-0928eb3a4874','c289101e-4052-426d-8442-70942392e7f1','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=7UuHyBsUSB8','youtube','Nightcore Classics','Rockefeller Street [HD]','7UuHyBsUSB8','https://img.youtube.com/vi/7UuHyBsUSB8/hqdefault.jpg','2026-07-23T22:13:21.419224');
INSERT INTO "songs" VALUES('5155dce4-14c8-4daf-88fb-2d42acd0e773','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://music.youtube.com/watch?v=BNyYiTdqzAY','youtube','Desconocido','And Plague Flowers the Kaleidoscope','BNyYiTdqzAY','https://img.youtube.com/vi/BNyYiTdqzAY/hqdefault.jpg','2026-07-24T00:28:46.543281');
INSERT INTO "songs" VALUES('e09da285-ef9b-4b74-abff-a4d096418196','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219','68179ce1-adf3-4027-9a6b-ef15746d0282','https://music.youtube.com/watch?v=hYIovLXa7M4','youtube','Desconocido','Goretex','hYIovLXa7M4','https://img.youtube.com/vi/hYIovLXa7M4/hqdefault.jpg','2026-07-24T00:40:03.037391');
INSERT INTO "songs" VALUES('cc6bc85c-1ad5-4762-af68-208f156a0f19','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://music.youtube.com/watch?v=MzkmcVQTPE0','youtube','Desconocido','Que Calor','MzkmcVQTPE0','https://img.youtube.com/vi/MzkmcVQTPE0/hqdefault.jpg','2026-07-24T00:40:47.559144');
INSERT INTO "songs" VALUES('a67c1997-55cb-466f-8e38-b33bec0c74f4','3c70b9e6-d45a-453d-9381-49a37139e131','68179ce1-adf3-4027-9a6b-ef15746d0282','https://music.youtube.com/watch?v=06INp4j-y6Q&si=YqhVARdtWsIl_6cN','youtube','Desconocido','Engraved Subdermal Dog-Tag','06INp4j-y6Q','https://img.youtube.com/vi/06INp4j-y6Q/hqdefault.jpg','2026-07-24T11:41:18.812236');
INSERT INTO "songs" VALUES('9e897f20-6d3d-44a5-99e2-02d630936874','3c70b9e6-d45a-453d-9381-49a37139e131','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://music.youtube.com/watch?v=PV81Ymo5Ohs&si=qiNvufrHFIr_88Wf','youtube','Desconocido','Noche Without You','PV81Ymo5Ohs','https://img.youtube.com/vi/PV81Ymo5Ohs/hqdefault.jpg','2026-07-24T11:47:34.404752');
INSERT INTO "songs" VALUES('03ee946a-13c5-459b-8d66-39690244e403','618d35d5-de73-4066-aaa3-e2f4f8589378','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://youtu.be/mJPG2RxJ6RE','youtube','Desconocido','イニシエノウタ/デボル','mJPG2RxJ6RE','https://img.youtube.com/vi/mJPG2RxJ6RE/hqdefault.jpg','2026-07-24T17:38:39.877372');
INSERT INTO "songs" VALUES('1e4df8a4-830b-4fa1-8671-8d820f1a0ded','d790be9d-6cf5-4975-b442-580503242362','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=OAoQLkXiruo','youtube','Kobaryo','fun TIME (Omega 2.0 Edit) [TANO*C TOUR 2024 TOKYO]','OAoQLkXiruo','https://img.youtube.com/vi/OAoQLkXiruo/hqdefault.jpg','2026-07-24T21:42:08.869902');
INSERT INTO "songs" VALUES('301d6246-f813-4aab-8c2e-474d5adad820','d790be9d-6cf5-4975-b442-580503242362','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://music.youtube.com/watch?v=GmhwtGRgMRA&si=-RHnLjFHjUIw0t_A','youtube','Desconocido','Harder To Pretend','GmhwtGRgMRA','https://img.youtube.com/vi/GmhwtGRgMRA/hqdefault.jpg','2026-07-24T21:51:09.577293');
INSERT INTO "songs" VALUES('82f254ea-fc4b-4f97-82fa-903795e7d5a7','1cfb0503-265e-424c-a912-a252058da58a','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=qc98u-eGzlc&list=RDqc98u-eGzlc','youtube','MESHUGGAH','Bleed (Official Music Video)','qc98u-eGzlc','https://img.youtube.com/vi/qc98u-eGzlc/hqdefault.jpg','2026-07-25T23:54:10.0314');
INSERT INTO "songs" VALUES('5d042b99-5a1c-4c26-b82f-fc026dcfe5bd','1cfb0503-265e-424c-a912-a252058da58a','4bad44ad-39da-49e3-aa07-8ccde6945cc2','https://www.youtube.com/watch?v=-lAI5QFXEFM&list=RD-lAI5QFXEFM','youtube','David Darling','Lugu Lugu Kan-Ibi','-lAI5QFXEFM','https://img.youtube.com/vi/-lAI5QFXEFM/hqdefault.jpg','2026-07-25T23:55:32.742277');
INSERT INTO "songs" VALUES('1311ae12-b66e-4e1c-a4d9-191db4bc977f','1cfb0503-265e-424c-a912-a252058da58a','68179ce1-adf3-4027-9a6b-ef15746d0282','https://www.youtube.com/watch?v=dw-7MXEW7mI&list=RDdw-7MXEW7mI','youtube','Señor Coconut','Electrolatino (Ricardo Villalobos'' ''Lecktro Cariño Mix)','dw-7MXEW7mI','https://img.youtube.com/vi/dw-7MXEW7mI/hqdefault.jpg','2026-07-26T00:00:53.535494');
INSERT INTO "songs" VALUES('84a29e1c-459a-4a8e-a137-3035553c7db1','d790be9d-6cf5-4975-b442-580503242362','db7569b7-7863-45f2-bea9-07d01eab5bf0','https://www.youtube.com/watch?v=3khI3vqV0FY','youtube','Loathe','Revenant (Official Music Video)','3khI3vqV0FY','https://img.youtube.com/vi/3khI3vqV0FY/hqdefault.jpg','2026-07-26T20:54:04.016439');
INSERT INTO "songs" VALUES('146adbd8-1cba-4a4d-8f34-de8c1b4aa84a','d790be9d-6cf5-4975-b442-580503242362','68179ce1-adf3-4027-9a6b-ef15746d0282','https://youtu.be/SQ45EWhhtHc?si=mQmCXCcfL_eTqv8q','youtube','Ruby My Dear','Kismet','SQ45EWhhtHc','https://img.youtube.com/vi/SQ45EWhhtHc/hqdefault.jpg','2026-07-26T23:23:41.004344');
INSERT INTO "songs" VALUES('a7a72977-5372-443e-b27b-fa2ad3ccf1d9','3c70b9e6-d45a-453d-9381-49a37139e131','68179ce1-adf3-4027-9a6b-ef15746d0282','https://music.youtube.com/watch?v=V9Suvx0K5Eo&si=ODzmFHFCOVwAggs-','youtube','Desconocido','Free Your Mind','V9Suvx0K5Eo','https://img.youtube.com/vi/V9Suvx0K5Eo/hqdefault.jpg','2026-08-06T12:38:19.87985');
INSERT INTO "songs" VALUES('26a19d4a-97d7-4f33-81d8-0ef21b8882ed','760ef44a-f400-40c2-941a-afe0a9b6fd48','bc881bdb-77ba-4393-9d85-8a96767735f2','https://youtube.com/watch?v=123','youtube','Artista Test','Canción Test',NULL,NULL,'2026-08-14T00:00:00Z');
CREATE TABLE users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar_url TEXT,
            is_approved INTEGER DEFAULT 1,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );
INSERT INTO "users" VALUES('1cfb0503-265e-424c-a912-a252058da58a','davilon18703@gmail.com','spruti the superputi','365e5f7e3d0a155651fc71fdb971cbd1:646f21849485a6dd3856431c4fd31373f9fbbeacbcd3f47c781e5c0f710413c1','https://api.dicebear.com/7.x/pixel-art/svg?seed=spruti the superputi',1,0,'2026-07-25 22:36:20.040704+00:00');
INSERT INTO "users" VALUES('be5771f5-a5b5-4161-a10e-4bd489701ca5','rigurima@gmail.com','Rigurima','a180caeda64cd1ed0be8303315743ae7:1ce658abfb2cf98d934f27f90daa0febbd6d3399dede40f181be95a03f8e0baf','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/be5771f5-a5b5-4161-a10e-4bd489701ca5_avatar.png',1,0,'2026-07-24 22:27:20.455762+00:00');
INSERT INTO "users" VALUES('618d35d5-de73-4066-aaa3-e2f4f8589378','phxdoris@gmail.com','dori','426668d4c1734569df233a8f9dcbea19:f1ff19ff16fb35ee79ad219bb5299f96ff866a191af1e2ee4caf1dd6c232518d','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/618d35d5-de73-4066-aaa3-e2f4f8589378_avatar.png',1,0,'2026-07-24 13:07:07.403107+00:00');
INSERT INTO "users" VALUES('e08a8951-39f5-4694-b0bf-7b1f0e7c6e71','joseluis1234595@gmail.com','Emeraldking6','0cfd6c5df3baf7448271193f2b13b68c:d43bb58a63666d520eb6177403627f50ebd268f0b537f354e8d2095ebbfc7f01','https://api.dicebear.com/7.x/pixel-art/svg?seed=Emeraldking6',1,0,'2026-07-24 06:03:09.407272+00:00');
INSERT INTO "users" VALUES('2956e27a-aa67-4e1c-bafb-15437ad37d43','davidbrotons2@gmail.com','Kuro','fe1262530a9d120ddfb4613cdee2adbf:69c115d0bb75dc14f3107ea35f8df1abf3c35980fb2cefa4c399bc76be18742d','https://api.dicebear.com/7.x/pixel-art/svg?seed=Kuro',1,0,'2026-07-24 00:52:33.081670+00:00');
INSERT INTO "users" VALUES('13b3423d-84e3-4c70-8812-84cca8ac567b','szxryxeras@gmail.com','xanaeras','cc8f1ef48ba6feb37e104e7c9577c3e5:0d53bcc13636b6152feb73f28e488810cef702abc48d10e806466971a5a30a83','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/13b3423d-84e3-4c70-8812-84cca8ac567b_avatar.png',1,0,'2026-07-23 21:59:16.242978+00:00');
INSERT INTO "users" VALUES('c289101e-4052-426d-8442-70942392e7f1','joserodrijimenez2001@gmail.com','MoneteCosmico','75b3663e53ea469a19f7b4d3091f317d:6a5911f617c9fcfe738df32bd268809578498ac936c53d06838bfba1c1baa9ee','https://api.dicebear.com/7.x/pixel-art/svg?seed=MoneteCosmico',1,0,'2026-07-23 21:47:51.801606+00:00');
INSERT INTO "users" VALUES('9c98ef89-18ff-43a5-b4c2-f0bb83b0e219','neospacio@hotmail.es','nekoamistad','ceeb7617ef2d95364818d4f787589e19:372705b0d312b4fc211c6c76165376861fd29f9acd68eded7764f1f7f918b5d1','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/9c98ef89-18ff-43a5-b4c2-f0bb83b0e219_avatar.png',1,0,'2026-07-23 19:47:33.125466+00:00');
INSERT INTO "users" VALUES('3c70b9e6-d45a-453d-9381-49a37139e131','linkeriyo@gmail.com','linkeriyo','e42eb1db71b9ee11e06d67d81507903d:6f62b541dfa2d3a9825324ba56733e6070687d5f46d4ff64e92f6dacd1ea3054','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/3c70b9e6-d45a-453d-9381-49a37139e131_avatar.png',1,0,'2026-07-23 11:16:14.889704+00:00');
INSERT INTO "users" VALUES('bbcfa206-4dc8-46f3-9618-911bc660c963','erikasolarico@outlook.com','FENTANILO','415cc5884448ed73135513d68e0609be:8c0883ce91ec9ea34c64c621fd077f686824e074810dcd2b2e7e6660043c7271','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/bbcfa206-4dc8-46f3-9618-911bc660c963_avatar.png',1,0,'2026-07-22 20:16:59.371940+00:00');
INSERT INTO "users" VALUES('05f12efd-bd86-4ee8-b557-febe3cce05a8','uneudysis@gmail.com','EUDY','696a223bfe8cef9b5e3e9564ed763938:ae998b304f6f9fd0468f71ed1ce3054434635e951c9520df21f028aae3df802b','https://api.dicebear.com/7.x/pixel-art/svg?seed=EUDY',1,0,'2026-07-21 18:33:34.656825+00:00');
INSERT INTO "users" VALUES('bf898c63-fd09-4d94-a7ed-a74e36861ca0','aurredits@gmail.com','Pol','7dd01a8ef9292bc1aaa61e1db1f19afe:c206c0c5b75de953d5048f9ed6f8789308270670a425217671a19c40c26b2c50','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/bf898c63-fd09-4d94-a7ed-a74e36861ca0_avatar.png',1,0,'2026-07-21 18:08:31.144555+00:00');
INSERT INTO "users" VALUES('d8e22bc5-da10-4fea-810b-9f8f3221e205','marblefade777@gmail.com','capoeirafalso','bd22f256033d072b1b330d5deeb4a6f0:44072080aa5d09031650f8fc992f462d84652b18e191dc75ab99870bf6e0c9df','https://api.dicebear.com/7.x/pixel-art/svg?seed=capoeirafalso',1,0,'2026-07-21 00:38:20.791472+00:00');
INSERT INTO "users" VALUES('c36e4f88-1e85-4a5a-a447-bc0555b3c0ed','canelakinta@gmail.com','cristian','4a235b1aab461f862659ac673a8fb723:92807a50f9da6298e709754609254ece362eddb971192e49ba82bb5f079e023c','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/c36e4f88-1e85-4a5a-a447-bc0555b3c0ed_avatar.png',1,1,'2026-07-12 17:15:47.713632+00:00');
INSERT INTO "users" VALUES('d790be9d-6cf5-4975-b442-580503242362','navpercris@gmail.com','capoeira','eee4f6cee840a20c5ad50ac5dcf059e8:b47a0b7ac0afc42982d00f27596bbfd7013577c9b7cf1a4fe9a944b70a662d92','https://vdgtskjbifgduzkspjqj.supabase.co/storage/v1/object/public/avatars/d790be9d-6cf5-4975-b442-580503242362_avatar.png',1,1,'2026-07-11 00:38:53.651518+00:00');
INSERT INTO "users" VALUES('760ef44a-f400-40c2-941a-afe0a9b6fd48','admin@dorisk.com','AdminTest','48d752b83835c45f798f7bdcda93f31e:30ee182ac8799180ba39132f574b16b726b27cfc7a8a083134b7209945d752d4',NULL,1,0,'2026-08-14T00:00:00Z');
CREATE TABLE votes (
            song_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (song_id, user_id),
            FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
INSERT INTO "votes" VALUES('7f974795-29fc-45dd-b302-52c160fdd4e0','a4c82220-a7d9-4b47-9ecc-023d39363a8f',7,'2026-08-14T00:00:00Z');
INSERT INTO "votes" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',5,'2026-07-24T00:34:51.583258');
INSERT INTO "votes" VALUES('f167a0f9-7ca4-41ff-bd0d-0928eb3a4874','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',7,'2026-07-24T00:35:22.969878');
INSERT INTO "votes" VALUES('b420d7be-7e1b-4fb9-a4b7-166db896f8ad','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',7,'2026-07-24T00:36:09.271835');
INSERT INTO "votes" VALUES('b420d7be-7e1b-4fb9-a4b7-166db896f8ad','d790be9d-6cf5-4975-b442-580503242362',6,'2026-07-24T00:37:02.661608');
INSERT INTO "votes" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','d790be9d-6cf5-4975-b442-580503242362',5,'2026-07-24T00:37:34.180678');
INSERT INTO "votes" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',7,'2026-07-24T00:37:44.335746');
INSERT INTO "votes" VALUES('1e748911-6cdc-4452-9f5a-3a760c1b439b','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',5,'2026-07-24T00:37:50.376269');
INSERT INTO "votes" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',4,'2026-07-24T00:38:44.032861');
INSERT INTO "votes" VALUES('539dd2b9-88d9-4d82-a099-0b7a0460f0b1','bf898c63-fd09-4d94-a7ed-a74e36861ca0',3,'2026-07-24T06:47:25.967708');
INSERT INTO "votes" VALUES('2ade6604-1b2c-4674-a3fc-d87bc8c1644f','bf898c63-fd09-4d94-a7ed-a74e36861ca0',3,'2026-07-24T06:47:38.165661');
INSERT INTO "votes" VALUES('cc6bc85c-1ad5-4762-af68-208f156a0f19','3c70b9e6-d45a-453d-9381-49a37139e131',6,'2026-07-24T11:38:37.756208');
INSERT INTO "votes" VALUES('2ade6604-1b2c-4674-a3fc-d87bc8c1644f','3c70b9e6-d45a-453d-9381-49a37139e131',4,'2026-07-23T23:50:14.984663');
INSERT INTO "votes" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','bf898c63-fd09-4d94-a7ed-a74e36861ca0',3,'2026-07-23T19:52:12.286732');
INSERT INTO "votes" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','bbcfa206-4dc8-46f3-9618-911bc660c963',5,'2026-07-23T20:01:49.234212');
INSERT INTO "votes" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','bbcfa206-4dc8-46f3-9618-911bc660c963',5,'2026-07-23T20:01:53.461931');
INSERT INTO "votes" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','bbcfa206-4dc8-46f3-9618-911bc660c963',5,'2026-07-23T20:08:23.557056');
INSERT INTO "votes" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','bbcfa206-4dc8-46f3-9618-911bc660c963',4,'2026-07-23T20:08:44.007488');
INSERT INTO "votes" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','3c70b9e6-d45a-453d-9381-49a37139e131',7,'2026-07-23T20:17:56.014769');
INSERT INTO "votes" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','3c70b9e6-d45a-453d-9381-49a37139e131',5,'2026-07-23T20:20:31.848799');
INSERT INTO "votes" VALUES('ac8afbab-8b06-49a6-bb0d-80ca4995eb76','3c70b9e6-d45a-453d-9381-49a37139e131',3,'2026-07-23T20:22:02.43788');
INSERT INTO "votes" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','3c70b9e6-d45a-453d-9381-49a37139e131',4,'2026-07-23T20:22:48.627514');
INSERT INTO "votes" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','d790be9d-6cf5-4975-b442-580503242362',4,'2026-07-23T20:23:27.663464');
INSERT INTO "votes" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','3c70b9e6-d45a-453d-9381-49a37139e131',3,'2026-07-23T20:23:49.278734');
INSERT INTO "votes" VALUES('1e748911-6cdc-4452-9f5a-3a760c1b439b','3c70b9e6-d45a-453d-9381-49a37139e131',3,'2026-07-23T20:24:37.066933');
INSERT INTO "votes" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','bf898c63-fd09-4d94-a7ed-a74e36861ca0',4,'2026-07-23T20:28:33.460717');
INSERT INTO "votes" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','bf898c63-fd09-4d94-a7ed-a74e36861ca0',5,'2026-07-23T20:32:06.291795');
INSERT INTO "votes" VALUES('e4b28f21-b12c-418d-a165-3215bdfcb2dc','bf898c63-fd09-4d94-a7ed-a74e36861ca0',5,'2026-07-23T20:32:24.316103');
INSERT INTO "votes" VALUES('5155dce4-14c8-4daf-88fb-2d42acd0e773','3c70b9e6-d45a-453d-9381-49a37139e131',6,'2026-07-24T11:39:16.49214');
INSERT INTO "votes" VALUES('e09da285-ef9b-4b74-abff-a4d096418196','3c70b9e6-d45a-453d-9381-49a37139e131',5,'2026-07-24T11:40:27.93045');
INSERT INTO "votes" VALUES('1e748911-6cdc-4452-9f5a-3a760c1b439b','d790be9d-6cf5-4975-b442-580503242362',3,'2026-07-24T17:23:16.208346');
INSERT INTO "votes" VALUES('f167a0f9-7ca4-41ff-bd0d-0928eb3a4874','d790be9d-6cf5-4975-b442-580503242362',2,'2026-07-24T17:23:22.200391');
INSERT INTO "votes" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','bf898c63-fd09-4d94-a7ed-a74e36861ca0',4,'2026-07-23T20:35:35.462103');
INSERT INTO "votes" VALUES('ac8afbab-8b06-49a6-bb0d-80ca4995eb76','bf898c63-fd09-4d94-a7ed-a74e36861ca0',2,'2026-07-23T20:35:30.890339');
INSERT INTO "votes" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','3c70b9e6-d45a-453d-9381-49a37139e131',2,'2026-07-23T20:39:47.569409');
INSERT INTO "votes" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','3c70b9e6-d45a-453d-9381-49a37139e131',5,'2026-07-23T20:44:11.594122');
INSERT INTO "votes" VALUES('014af269-6ce8-4e89-9540-41e0f4cab733','bbcfa206-4dc8-46f3-9618-911bc660c963',4,'2026-07-23T21:49:29.803448');
INSERT INTO "votes" VALUES('b420d7be-7e1b-4fb9-a4b7-166db896f8ad','bbcfa206-4dc8-46f3-9618-911bc660c963',5,'2026-07-23T21:49:48.32769');
INSERT INTO "votes" VALUES('e4b28f21-b12c-418d-a165-3215bdfcb2dc','c289101e-4052-426d-8442-70942392e7f1',4,'2026-07-23T21:51:22.463847');
INSERT INTO "votes" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','c289101e-4052-426d-8442-70942392e7f1',4,'2026-07-23T21:52:11.810311');
INSERT INTO "votes" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','c289101e-4052-426d-8442-70942392e7f1',6,'2026-07-23T21:52:26.16754');
INSERT INTO "votes" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','c289101e-4052-426d-8442-70942392e7f1',5,'2026-07-23T21:55:56.236975');
INSERT INTO "votes" VALUES('014af269-6ce8-4e89-9540-41e0f4cab733','c289101e-4052-426d-8442-70942392e7f1',2,'2026-07-23T21:57:44.973883');
INSERT INTO "votes" VALUES('ac8afbab-8b06-49a6-bb0d-80ca4995eb76','c289101e-4052-426d-8442-70942392e7f1',6,'2026-07-23T21:58:56.47709');
INSERT INTO "votes" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','c289101e-4052-426d-8442-70942392e7f1',5,'2026-07-23T22:01:01.336442');
INSERT INTO "votes" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','618d35d5-de73-4066-aaa3-e2f4f8589378',2,'2026-07-24T17:43:30.71122');
INSERT INTO "votes" VALUES('d7bdeaf9-fc0d-456a-9815-77c495079cac','c289101e-4052-426d-8442-70942392e7f1',4,'2026-07-23T22:02:00.290398');
INSERT INTO "votes" VALUES('b420d7be-7e1b-4fb9-a4b7-166db896f8ad','c289101e-4052-426d-8442-70942392e7f1',4,'2026-07-23T22:03:30.902988');
INSERT INTO "votes" VALUES('1e748911-6cdc-4452-9f5a-3a760c1b439b','c289101e-4052-426d-8442-70942392e7f1',2,'2026-07-23T22:04:19.349673');
INSERT INTO "votes" VALUES('77fe3891-78b3-49ed-a069-974522885dbb','c289101e-4052-426d-8442-70942392e7f1',6,'2026-07-23T22:05:31.541176');
INSERT INTO "votes" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','c289101e-4052-426d-8442-70942392e7f1',7,'2026-07-23T22:07:35.641833');
INSERT INTO "votes" VALUES('539dd2b9-88d9-4d82-a099-0b7a0460f0b1','3c70b9e6-d45a-453d-9381-49a37139e131',4,'2026-07-23T23:47:59.444903');
INSERT INTO "votes" VALUES('f167a0f9-7ca4-41ff-bd0d-0928eb3a4874','3c70b9e6-d45a-453d-9381-49a37139e131',6,'2026-07-23T23:48:14.359529');
INSERT INTO "votes" VALUES('73864d81-0228-41ad-82fe-c8fd3ff3256c','3c70b9e6-d45a-453d-9381-49a37139e131',5,'2026-07-23T20:25:40.000372');
INSERT INTO "votes" VALUES('539dd2b9-88d9-4d82-a099-0b7a0460f0b1','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',4,'2026-07-24T00:18:41.824158');
INSERT INTO "votes" VALUES('e4b28f21-b12c-418d-a165-3215bdfcb2dc','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',7,'2026-07-24T00:19:13.106961');
INSERT INTO "votes" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',4,'2026-07-24T00:20:06.533993');
INSERT INTO "votes" VALUES('9183d8b0-36a2-4464-8308-4f710bd95fe2','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',6,'2026-07-24T00:20:39.36681');
INSERT INTO "votes" VALUES('2ade6604-1b2c-4674-a3fc-d87bc8c1644f','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',5,'2026-07-24T00:29:34.808741');
INSERT INTO "votes" VALUES('014af269-6ce8-4e89-9540-41e0f4cab733','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',6,'2026-07-24T00:31:13.89611');
INSERT INTO "votes" VALUES('ac8afbab-8b06-49a6-bb0d-80ca4995eb76','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',4,'2026-07-24T00:31:56.052407');
INSERT INTO "votes" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',5,'2026-07-24T00:33:20.069362');
INSERT INTO "votes" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','618d35d5-de73-4066-aaa3-e2f4f8589378',1,'2026-07-24T17:43:31.660908');
INSERT INTO "votes" VALUES('b6ddaf41-0379-450d-a396-1587d5076cf4','618d35d5-de73-4066-aaa3-e2f4f8589378',1,'2026-07-24T17:43:32.410107');
INSERT INTO "votes" VALUES('03ee946a-13c5-459b-8d66-39690244e403','9c98ef89-18ff-43a5-b4c2-f0bb83b0e219',7,'2026-07-24T17:46:01.904967');
INSERT INTO "votes" VALUES('cc6bc85c-1ad5-4762-af68-208f156a0f19','d790be9d-6cf5-4975-b442-580503242362',4,'2026-07-24T21:51:44.297589');
INSERT INTO "votes" VALUES('bf1c15ed-b396-42bb-af78-30d51c147a3e','d790be9d-6cf5-4975-b442-580503242362',6,'2026-07-24T21:51:56.015005');
INSERT INTO "votes" VALUES('e4b28f21-b12c-418d-a165-3215bdfcb2dc','d790be9d-6cf5-4975-b442-580503242362',2,'2026-07-24T22:01:56.104017');
INSERT INTO "votes" VALUES('539dd2b9-88d9-4d82-a099-0b7a0460f0b1','d790be9d-6cf5-4975-b442-580503242362',2,'2026-07-24T22:02:45.620362');
INSERT INTO "votes" VALUES('03ee946a-13c5-459b-8d66-39690244e403','d790be9d-6cf5-4975-b442-580503242362',4,'2026-07-24T22:02:58.383214');
INSERT INTO "votes" VALUES('9e897f20-6d3d-44a5-99e2-02d630936874','d790be9d-6cf5-4975-b442-580503242362',3,'2026-07-24T22:03:19.743108');
INSERT INTO "votes" VALUES('e09da285-ef9b-4b74-abff-a4d096418196','d790be9d-6cf5-4975-b442-580503242362',3,'2026-07-25T22:39:14.220331');
INSERT INTO "votes" VALUES('a67c1997-55cb-466f-8e38-b33bec0c74f4','d790be9d-6cf5-4975-b442-580503242362',5,'2026-07-25T22:39:21.127027');
INSERT INTO "votes" VALUES('91b02e26-c228-4380-a669-345536f0d0b0','d790be9d-6cf5-4975-b442-580503242362',4,'2026-07-27T22:41:07.543572');
INSERT INTO "votes" VALUES('26a19d4a-97d7-4f33-81d8-0ef21b8882ed','760ef44a-f400-40c2-941a-afe0a9b6fd48',7,'2026-08-14T00:00:00Z');
CREATE TABLE weekly_winners (
            id TEXT PRIMARY KEY,
            playlist_id TEXT,
            week_label TEXT NOT NULL,
            track TEXT NOT NULL,
            artist TEXT NOT NULL,
            submitted_by TEXT NOT NULL,
            score REAL NOT NULL,
            trophy TEXT NOT NULL,
            art_url TEXT,
            created_at TEXT NOT NULL
        );
INSERT INTO "weekly_winners" VALUES('931dd325-4c5c-4bcc-9946-3f3823e4de0c','f8ce0f25-cd9b-4b42-8ed2-682e20e0f2db','SEMANA 31 (06 AUG - 13 AUG) · TEST PLAYLIST','Canción Test','Artista Test','@AdminTest',7.0,'🏆',NULL,'2026-08-13T22:16:48.819502+00:00');
INSERT INTO "weekly_winners" VALUES('ff024e41-c49c-495d-b6c0-fe61f38c647e','3208f373-d0f4-4271-bff6-16357fda0589','SEMANA 31 (06 AUG - 13 AUG) · TEST PLAYLIST','Canción Test','Artista Test','@AdminTest',7.0,'🏆',NULL,'2026-08-13T22:17:11.831682+00:00');
INSERT INTO "weekly_winners" VALUES('f17ad692-897f-4409-a52b-6f47f17b96de','bc881bdb-77ba-4393-9d85-8a96767735f2','SEMANA 31 (09 AUG - 16 AUG) · TEST PLAYLIST','Canción Test','Artista Test','@AdminTest',7.0,'🏆',NULL,'2026-08-16T17:59:37.697200+00:00');
COMMIT;