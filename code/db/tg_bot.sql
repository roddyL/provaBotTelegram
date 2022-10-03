-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Set 29, 2022 alle 17:28
-- Versione del server: 10.4.22-MariaDB
-- Versione PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tg_bot`
--

-- --------------------------------------------------------

--
-- Struttura stand-in per le viste `empty_seats`
-- (Vedi sotto per la vista effettiva)
--
CREATE TABLE `empty_seats` (
`data` date
,`fascia_oraria` varchar(15)
,`posti_disponibili` decimal(33,0)
);

-- --------------------------------------------------------

--
-- Struttura stand-in per le viste `empty_seats_prova`
-- (Vedi sotto per la vista effettiva)
--
CREATE TABLE `empty_seats_prova` (
`data` date
,`fascia_oraria` varchar(15)
,`posti_disp` decimal(34,0)
);

-- --------------------------------------------------------

--
-- Struttura stand-in per le viste `empty_seats_v2`
-- (Vedi sotto per la vista effettiva)
--
CREATE TABLE `empty_seats_v2` (
`data` date
,`fascia_oraria` varchar(15)
,`nome_ufficio` varchar(20)
,`posti_disponibili` decimal(34,0)
);

-- --------------------------------------------------------

--
-- Struttura della tabella `evento`
--

CREATE TABLE `evento` (
  `id` tinyint(3) NOT NULL,
  `nome_evento` varchar(64) NOT NULL,
  `posti` int(5) NOT NULL,
  `datetime` datetime NOT NULL,
  `descrizione` varchar(256) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `prenotazione`
--

CREATE TABLE `prenotazione` (
  `id` int(5) NOT NULL,
  `id_prenotazione` varchar(20) NOT NULL,
  `telegram_id` bigint(64) NOT NULL,
  `nome_ufficio` varchar(20) NOT NULL,
  `posti_prenotati` int(3) UNSIGNED NOT NULL,
  `fascia_oraria` varchar(15) NOT NULL,
  `data` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `prenotazione`
--

INSERT INTO `prenotazione` (`id`, `id_prenotazione`, `telegram_id`, `nome_ufficio`, `posti_prenotati`, `fascia_oraria`, `data`, `timestamp`) VALUES
(101, '2022-09-29_1', 224239481, 'liveDemo+9', 10, 'mattino', '2022-09-29', '2022-09-27 08:11:21'),
(102, '2022-09-29_1', 224239481, 'liveDemo+9', 10, 'pomeriggio', '2022-09-29', '2022-09-27 08:11:21'),
(103, '2022-09-30_1', 224239481, 'liveDemo+3', 2, 'mattino', '2022-09-30', '2022-09-29 06:00:20'),
(104, '2022-09-30_1', 224239481, 'liveDemo+3', 2, 'pomeriggio', '2022-09-30', '2022-09-29 06:00:20'),
(109, '2022-09-30_2', 563678634, 'liveDemo+9', 3, 'mattino', '2022-09-30', '2022-09-29 12:56:30'),
(110, '2022-09-30_2', 563678634, 'liveDemo+9', 3, 'pomeriggio', '2022-09-30', '2022-09-29 12:56:30'),
(111, '2022-09-30_3', 224239481, 'liveDemo+9', 4, 'mattino', '2022-09-30', '2022-09-29 12:56:50'),
(112, '2022-09-30_3', 224239481, 'liveDemo+9', 4, 'pomeriggio', '2022-09-30', '2022-09-29 12:56:50'),
(113, '2022-10-06_1', 5040854072, 'liveDemo+9', 20, 'mattino', '2022-10-06', '2022-09-29 13:45:38'),
(114, '2022-10-06_1', 5040854072, 'liveDemo+9', 20, 'pomeriggio', '2022-10-06', '2022-09-29 13:45:38'),
(107, '2022-10-13_1', 563678634, 'liveDemo+9', 16, 'mattino', '2022-10-13', '2022-09-29 12:55:47'),
(108, '2022-10-13_1', 563678634, 'liveDemo+9', 16, 'pomeriggio', '2022-10-13', '2022-09-29 12:55:47'),
(105, '2022-10-18_1', 563678634, 'liveDemo+3', 10, 'mattino', '2022-10-18', '2022-09-29 09:20:08'),
(106, '2022-10-18_1', 563678634, 'liveDemo+3', 10, 'pomeriggio', '2022-10-18', '2022-09-29 09:20:08'),
(115, '2022-10-21_1', 5040854072, 'liveDemo+3', 10, 'pomeriggio', '2022-10-21', '2022-09-29 13:46:01');

--
-- Trigger `prenotazione`
--
DELIMITER $$
CREATE TRIGGER `check_seats_v2` BEFORE UPDATE ON `prenotazione` FOR EACH ROW IF NEW.posti_prenotati>(select posti_disponibili 
from `tg_bot`.`empty_seats_v2` as e2
where e2.la_data=NEW.data AND e2.fascia_oraria=NEW.fascia_oraria) THEN
            signal sqlstate '45000'
            set message_text = 'il valore dei posti disponibili è inferiore al valore dei posti prenotati';
        END IF
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `tr_check_seats` BEFORE INSERT ON `prenotazione` FOR EACH ROW IF NEW.posti_prenotati>(select `u`.`posti` - sum(`p`.`posti_prenotati`) from (`tg_bot`.`prenotazione` `p` join `tg_bot`.`ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where p.data=NEW.data AND p.fascia_oraria=NEW.fascia_oraria group by `p`.`data`,`p`.`fascia_oraria`) THEN
			signal sqlstate '45000'
			set message_text = 'il valore dei posti disponibili è inferiore al valore dei posti prenotati';
		END IF
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struttura della tabella `prova123`
--

CREATE TABLE `prova123` (
  `prova` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `ruolo`
--

CREATE TABLE `ruolo` (
  `id` tinyint(4) NOT NULL,
  `nome_ruolo` varchar(15) NOT NULL,
  `descrizione` varchar(256) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `livello_permesso` int(2) NOT NULL,
  `max_postiprenot` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `ruolo`
--

INSERT INTO `ruolo` (`id`, `nome_ruolo`, `descrizione`, `password`, `livello_permesso`, `max_postiprenot`) VALUES
(1, 'admin', 'amministratore', 'fromfarmtofork', 0, NULL),
(3, 'esterno', 'utente esterno verificato', 'smact2022', 2, NULL),
(2, 'guest', 'utente guest', NULL, 99, NULL),
(4, 'StagistiTOP', 'Siamo i mejo', 'TopSMACT', 0, -1);

-- --------------------------------------------------------

--
-- Struttura della tabella `sede`
--

CREATE TABLE `sede` (
  `id` int(11) NOT NULL,
  `nome_sede` varchar(20) NOT NULL,
  `citta` varchar(20) NOT NULL,
  `indirizzo_via` varchar(25) NOT NULL,
  `indirizzo_numeroCivico` varchar(3) NOT NULL,
  `longitudine` float NOT NULL,
  `latitudine` float NOT NULL,
  `descrizione` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `sede`
--

INSERT INTO `sede` (`id`, `nome_sede`, `citta`, `indirizzo_via`, `indirizzo_numeroCivico`, `longitudine`, `latitudine`, `descrizione`) VALUES
(1, 'fromfarmtofork', 'Padova', 'via Padova', '19', 46.4646, 69.697, 'la livedemo di padova');

-- --------------------------------------------------------

--
-- Struttura della tabella `ufficio`
--

CREATE TABLE `ufficio` (
  `id` int(5) NOT NULL,
  `nome_sede` varchar(20) NOT NULL,
  `nome_ufficio` varchar(20) NOT NULL,
  `descrizione` varchar(256) NOT NULL,
  `posti` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `ufficio`
--

INSERT INTO `ufficio` (`id`, `nome_sede`, `nome_ufficio`, `descrizione`, `posti`) VALUES
(2, 'fromfarmtofork', 'liveDemo+3', 'sala ufficio primo piano (scale all\'entrata)', 10),
(1, 'fromfarmtofork', 'liveDemo+9', '', 20);

-- --------------------------------------------------------

--
-- Struttura della tabella `utente`
--

CREATE TABLE `utente` (
  `Id` int(5) NOT NULL,
  `telegram_id` bigint(64) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `nome` varchar(30) DEFAULT NULL,
  `cognome` varchar(20) DEFAULT NULL,
  `recapito_telefonico` varchar(15) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `nome_ruolo` varchar(15) NOT NULL DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `utente`
--

INSERT INTO `utente` (`Id`, `telegram_id`, `username`, `nome`, `cognome`, `recapito_telefonico`, `mail`, `nome_ruolo`) VALUES
(129, 224239481, 'TunechiLiL', 'vivi', 'ggggg', '11111111111', 'lamaiaskhdis@mail.it', 'admin'),
(143, 563678634, 'ULTRon25', 'Fieno', 'Tanto', '8887778883', 'Sonoermejo@veneta.it', 'StagistiTOP'),
(163, 5040854072, 'None', 'Daniele', 'Sartori', '3333333333', NULL, 'admin');

-- --------------------------------------------------------

--
-- Struttura della tabella `whitelist`
--

CREATE TABLE `whitelist` (
  `id` int(5) NOT NULL,
  `telegram_id` bigint(64) NOT NULL,
  `is_logged` tinyint(1) NOT NULL DEFAULT 1,
  `dt_firstLogin` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `dt_lastLogin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `whitelist`
--

INSERT INTO `whitelist` (`id`, `telegram_id`, `is_logged`, `dt_firstLogin`, `dt_lastLogin`) VALUES
(54, 224239481, 1, '2022-09-29 15:05:27', '2022-09-29 15:05:27'),
(55, 563678634, 1, '2022-09-29 15:14:46', '2022-09-29 15:14:46'),
(56, 5040854072, 1, '2022-09-29 15:47:08', '2022-09-29 15:47:08');

-- --------------------------------------------------------

--
-- Struttura per vista `empty_seats`
--
DROP TABLE IF EXISTS `empty_seats`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `empty_seats`  AS SELECT `p`.`data` AS `data`, `p`.`fascia_oraria` AS `fascia_oraria`, `u`.`posti`- sum(`p`.`posti_prenotati`) AS `posti_disponibili` FROM (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) GROUP BY `p`.`data`, `p`.`fascia_oraria` ;

-- --------------------------------------------------------

--
-- Struttura per vista `empty_seats_prova`
--
DROP TABLE IF EXISTS `empty_seats_prova`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `empty_seats_prova`  AS   (select `a`.`data` AS `data`,`a`.`fascia_oraria` AS `fascia_oraria`,`a`.`posti` - (`a`.`posti_pren` + coalesce(`b`.`posti_pren`,0)) AS `posti_disp` from ((select `p`.`data` AS `data`,`p`.`fascia_oraria` AS `fascia_oraria`,`u`.`posti` AS `posti`,sum(`p`.`posti_prenotati`) AS `posti_pren` from (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where `p`.`fascia_oraria` <> 'intera giornata' group by `p`.`data`,`p`.`fascia_oraria`) `a` left join (select `p`.`data` AS `data`,`p`.`fascia_oraria` AS `fascia_oraria`,`p`.`posti_prenotati` AS `posti_pren` from (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where `p`.`fascia_oraria` = 'intera giornata') `b` on(`a`.`data` = `b`.`data`))) union (select `a`.`data` AS `data`,`a`.`fascia_oraria` AS `fascia_oraria`,`a`.`posti` - (`a`.`posti_pren` + coalesce(`b`.`posti_pren`,0)) AS `posti_disp` from ((select `p`.`data` AS `data`,`p`.`fascia_oraria` AS `fascia_oraria`,sum(`p`.`posti_prenotati`) AS `posti_pren` from (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where `p`.`fascia_oraria` = 'intera giornata' group by `p`.`data`,`p`.`fascia_oraria`) `b` left join (select `p`.`data` AS `data`,`p`.`fascia_oraria` AS `fascia_oraria`,`u`.`posti` AS `posti`,`p`.`posti_prenotati` AS `posti_pren` from (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where `p`.`fascia_oraria` <> 'intera giornata') `a` on(`a`.`data` = `b`.`data`)))  ;

-- --------------------------------------------------------

--
-- Struttura per vista `empty_seats_v2`
--
DROP TABLE IF EXISTS `empty_seats_v2`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `empty_seats_v2`  AS SELECT `a`.`DATA` AS `data`, `a`.`fascia_oraria` AS `fascia_oraria`, `a`.`nome_ufficio` AS `nome_ufficio`, `a`.`posti_disponibili`- coalesce(`b`.`posti_giornata`,0) AS `posti_disponibili` FROM ((select `p`.`data` AS `DATA`,`p`.`fascia_oraria` AS `fascia_oraria`,`p`.`nome_ufficio` AS `nome_ufficio`,`u`.`posti` - sum(`p`.`posti_prenotati`) AS `posti_disponibili` from (`prenotazione` `p` join `ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) where `p`.`fascia_oraria` <> 'intera giornata' group by `p`.`data`,`p`.`fascia_oraria`,`p`.`nome_ufficio`) `a` left join (select `g`.`data` AS `data`,`g`.`nome_ufficio` AS `nome_ufficio`,sum(`g`.`posti_prenotati`) AS `posti_giornata` from `prenotazione` `g` where `g`.`fascia_oraria` = 'intera giornata' group by `g`.`data`,`g`.`nome_ufficio`) `b` on(`a`.`nome_ufficio` = `b`.`nome_ufficio` and `a`.`DATA` = `b`.`data`)) ;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `evento`
--
ALTER TABLE `evento`
  ADD PRIMARY KEY (`nome_evento`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `prenotazione`
--
ALTER TABLE `prenotazione`
  ADD PRIMARY KEY (`id_prenotazione`,`fascia_oraria`),
  ADD KEY `id` (`id`),
  ADD KEY `nome_ufficio` (`nome_ufficio`),
  ADD KEY `telegram_id` (`telegram_id`);

--
-- Indici per le tabelle `ruolo`
--
ALTER TABLE `ruolo`
  ADD PRIMARY KEY (`nome_ruolo`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `sede`
--
ALTER TABLE `sede`
  ADD PRIMARY KEY (`nome_sede`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `ufficio`
--
ALTER TABLE `ufficio`
  ADD PRIMARY KEY (`nome_ufficio`),
  ADD KEY `id` (`id`),
  ADD KEY `nome_sede` (`nome_sede`);

--
-- Indici per le tabelle `utente`
--
ALTER TABLE `utente`
  ADD PRIMARY KEY (`telegram_id`),
  ADD KEY `Id` (`Id`),
  ADD KEY `nome_ruolo` (`nome_ruolo`);

--
-- Indici per le tabelle `whitelist`
--
ALTER TABLE `whitelist`
  ADD PRIMARY KEY (`telegram_id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `evento`
--
ALTER TABLE `evento`
  MODIFY `id` tinyint(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `prenotazione`
--
ALTER TABLE `prenotazione`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=116;

--
-- AUTO_INCREMENT per la tabella `ruolo`
--
ALTER TABLE `ruolo`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT per la tabella `sede`
--
ALTER TABLE `sede`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT per la tabella `ufficio`
--
ALTER TABLE `ufficio`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `utente`
--
ALTER TABLE `utente`
  MODIFY `Id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=164;

--
-- AUTO_INCREMENT per la tabella `whitelist`
--
ALTER TABLE `whitelist`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `prenotazione`
--
ALTER TABLE `prenotazione`
  ADD CONSTRAINT `prenotazione_ibfk_1` FOREIGN KEY (`nome_ufficio`) REFERENCES `ufficio` (`nome_ufficio`),
  ADD CONSTRAINT `prenotazione_ibfk_2` FOREIGN KEY (`telegram_id`) REFERENCES `utente` (`telegram_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ufficio`
--
ALTER TABLE `ufficio`
  ADD CONSTRAINT `ufficio_ibfk_1` FOREIGN KEY (`nome_sede`) REFERENCES `sede` (`nome_sede`);

--
-- Limiti per la tabella `utente`
--
ALTER TABLE `utente`
  ADD CONSTRAINT `utente_ibfk_1` FOREIGN KEY (`nome_ruolo`) REFERENCES `ruolo` (`nome_ruolo`);

--
-- Limiti per la tabella `whitelist`
--
ALTER TABLE `whitelist`
  ADD CONSTRAINT `whitelist_ibfk_1` FOREIGN KEY (`telegram_id`) REFERENCES `utente` (`telegram_id`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
--
-- Eventi
--
CREATE DEFINER=`root`@`localhost` EVENT `chiusura sessioni` ON SCHEDULE EVERY 3 HOUR STARTS '2022-07-19 00:00:00' ON COMPLETION PRESERVE ENABLE DO UPDATE whitelist SET is_logged = 0 WHERE DATEDIFF(CURRENT_TIMESTAMP, dt_lastLogin)>=4$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
