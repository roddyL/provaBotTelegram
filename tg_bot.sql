-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Lug 19, 2022 alle 17:58
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
-- Struttura della tabella `whitelist`
--

CREATE TABLE `whitelist` (
  `id` int(5) NOT NULL,
  `username` varchar(15) NOT NULL,
  `is_logged` tinyint(1) NOT NULL DEFAULT 1,
  `dt_firstLogin` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `dt_lastLogin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `whitelist`
--

INSERT INTO `whitelist` (`id`, `username`, `is_logged`, `dt_firstLogin`, `dt_lastLogin`) VALUES
(1, 'TunechiL1L', 1, '2022-07-19 17:56:49', '2022-07-16 15:51:59');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `whitelist`
--
ALTER TABLE `whitelist`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `whitelist`
--
ALTER TABLE `whitelist`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

DELIMITER $$
--
-- Eventi
--
CREATE DEFINER=`root`@`localhost` EVENT `chiusura sessioni` ON SCHEDULE EVERY 1 DAY STARTS '2022-07-19 00:00:00' ON COMPLETION PRESERVE ENABLE DO UPDATE whitelist SET is_logged = 0 WHERE DATEDIFF(CURRENT_TIMESTAMP, dt_lastLogin)>=4$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
