-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Ago 26, 2022 alle 17:55
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
-- Struttura della tabella `prenotazione`
--

CREATE TABLE `prenotazione` (
  `id` int(5) NOT NULL,
  `id_prenotazione` int(5) NOT NULL,
  `telegram_id` int(11) DEFAULT NULL,
  `nome_ufficio` varchar(20) NOT NULL,
  `posti_prenotati` int(3) NOT NULL,
  `fascia_oraria` varchar(15) NOT NULL,
  `data` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `latitudine` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `ufficio`
--

CREATE TABLE `ufficio` (
  `id` int(5) NOT NULL,
  `nome_sede` varchar(20) NOT NULL,
  `nome_ufficio` varchar(20) NOT NULL,
  `posti` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `utente`
--

CREATE TABLE `utente` (
  `Id` int(5) NOT NULL,
  `telegram_id` int(11) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Nome` varchar(30) NOT NULL,
  `Cognome` varchar(20) NOT NULL,
  `Recapito_telefonico` varchar(15) NOT NULL,
  `Mail` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `utente`
--

INSERT INTO `utente` (`Id`, `telegram_id`, `Username`, `Nome`, `Cognome`, `Recapito_telefonico`, `Mail`) VALUES
(7, 224239481, 'TunechiLiL', 'Ciao', 'Ciao', '11111111111', 'lamiamail@mail.it');

-- --------------------------------------------------------

--
-- Struttura della tabella `whitelist`
--

CREATE TABLE `whitelist` (
  `id` int(5) NOT NULL,
  `telegram_id` int(11) NOT NULL,
  `is_logged` tinyint(1) NOT NULL DEFAULT 1,
  `dt_firstLogin` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `dt_lastLogin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `whitelist`
--

INSERT INTO `whitelist` (`id`, `telegram_id`, `is_logged`, `dt_firstLogin`, `dt_lastLogin`) VALUES
(24, 224239481, 1, '2022-08-26 17:54:20', '2022-08-26 17:54:20');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `prenotazione`
--
ALTER TABLE `prenotazione`
  ADD PRIMARY KEY (`id_prenotazione`),
  ADD KEY `id` (`id`),
  ADD KEY `nome_ufficio` (`nome_ufficio`),
  ADD KEY `telegram_id` (`telegram_id`);

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
  ADD KEY `Username` (`Username`);

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
-- AUTO_INCREMENT per la tabella `prenotazione`
--
ALTER TABLE `prenotazione`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `sede`
--
ALTER TABLE `sede`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `ufficio`
--
ALTER TABLE `ufficio`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `utente`
--
ALTER TABLE `utente`
  MODIFY `Id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `whitelist`
--
ALTER TABLE `whitelist`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `prenotazione`
--
ALTER TABLE `prenotazione`
  ADD CONSTRAINT `prenotazione_ibfk_1` FOREIGN KEY (`nome_ufficio`) REFERENCES `ufficio` (`nome_ufficio`),
  ADD CONSTRAINT `prenotazione_ibfk_2` FOREIGN KEY (`telegram_id`) REFERENCES `utente` (`telegram_id`);

--
-- Limiti per la tabella `ufficio`
--
ALTER TABLE `ufficio`
  ADD CONSTRAINT `ufficio_ibfk_1` FOREIGN KEY (`nome_sede`) REFERENCES `sede` (`nome_sede`);

--
-- Limiti per la tabella `utente`
--
ALTER TABLE `utente`
  ADD CONSTRAINT `utente_ibfk_1` FOREIGN KEY (`telegram_id`) REFERENCES `whitelist` (`telegram_id`);

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
