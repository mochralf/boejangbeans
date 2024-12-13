-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2024 at 07:44 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `boejangbeans`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `salt` varchar(32) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `fname`, `lname`, `username`, `email`, `password_hash`, `salt`, `created_at`) VALUES
(1, 'Rafli', 'Prasetyo', 'Rafli', 'rafly4595@gmail.com', 'scrypt:32768:8:1$rGlsdUrrlFj4xiOk$f447711984ddfcbcd45a292b7e948a6141269fee8b726ae546d5987a2f30003a0ac5d5bacb1aadcb3ecad74d1c72a7c3bc86e9c07a814e692e98d511d7b0aa12', 'add200aa0db2c16f8e88c973317fe5f6', '2024-12-11 09:57:17'),
(2, 'Azzam', 'Mazzed', 'Azzam', 'mazeed@gmail.com', 'scrypt:32768:8:1$zGnjfiEjxw17Sffw$7f65007510be1b4e1fb201396d7b7fdfdb40c5793b5caeea30fc7654f366ad3d8839b81411fe42ed70ff230ae0096ccf02319e68db7e3bd58f44bfb958bb02f9', '6685bbd97fefa80ed2509066db3ef162', '2024-12-11 09:57:26'),
(3, 'Faqih', 'P', 'Faqih', 'deniardiansyah739@gmail.com', 'scrypt:32768:8:1$QUoHxJPDG8RENLkA$12cd1fd2b7cdd7e6f07e3c9be85906381987540ff7290a0168f5848a3bd2c02e65eb3bf1cfcfba605cdbe121e00e8c24f63e390d991d8a04c0724bc85f668f71', '11f165a1025276555d0dc4d015f7deb8', '2024-12-11 09:58:45'),
(4, 'Bayu', 'Wibu', 'Bayu', 'bayu13@gmail.com', 'scrypt:32768:8:1$DSEoBCXKrwCQFUzq$8f5b4ba475471dd3ed5e7faf8221b386065aecbafc8c81ce8f66c2eb133bb58e39b590ee146fb46468c942d1150abf7ec31feaede6a266ac9ac19236ed2a3c3f', 'c74379b82d4520cd07d811a915c407d4', '2024-12-12 16:39:53');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `nama` varchar(50) DEFAULT NULL,
  `harga` double DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `subTotal` double DEFAULT NULL,
  `pid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `no_hp` varchar(12) NOT NULL,
  `pesan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `nama`, `email`, `no_hp`, `pesan`) VALUES
(1, 'Rafli Ilham Prasetyo', 'rafly4595@gmail.com', '085155043588', 'Takde cawan kah ????');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `harga` varchar(11) NOT NULL,
  `stok` int(11) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `typeCoffee` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `nama`, `harga`, `stok`, `foto`, `typeCoffee`) VALUES
(1, 'Toraja Sapan 200gr', '105000', 20, '2.jpg', 'Strong'),
(2, 'Aceh Gayo Wine 200gr', '125000', 100, '2.jpg', 'Strong'),
(3, 'Aceh Gayo Honey 150gr', '94000', 80, '2.jpg', 'Low'),
(4, 'Bali Kintamani 200gr', '124000', 100, '2.jpg', 'Medium'),
(5, 'Flores Bajawa 200gr', '124000', 100, '2.jpg', 'Low'),
(6, 'Papua Paneli 200gr', '148000', 100, '2.jpg', 'Low'),
(9, 'Rafli Prasetyo', '145000', 55, '2.jpg', 'Medium');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
