<?php
/**
 * This file contains the main configuration as simple array
 */

// This sets the context the application is running in.
// It allows to change certain behavior depending on context.
// The currently supported contexts are:
// development		Used in the development environment
// production		Used on the live website
$context = @is_file(dirname( __FILE__ ) . DIRECTORY_SEPARATOR . 'developmentConfiguration.php') ? 'development' : 'production';
define('CONTEXT', $context);
define('SITE_ROOT', realpath(dirname(__FILE__) . DIRECTORY_SEPARATOR . '..' . DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR);

// The base configuration of the application
$configuration = array(
	// prepare dummy database settings (will be overridden by context depending configurations)
	'database' => array(
		'username'	=> 'root',
		'password'	=> 'venzTV4000606128',
		'name'		=> 'totalcom_addons',
		'server'	=> 'localhost',
	),
// addon dependencies to be met in order for them to be imported
//	'dependencies' => array(
//		'xbmc.python'	=> '2.1.0',
//		'xbmc.gui'		=> '5.0.0'
//	),
	// defines some settings needed to interact with the repositories
	'repositories' => array(
		'xboxskins' => array ( 'name' => 'XBMC4Xbox Skins Repository', 'dataUrl' => 'https://github.com/noobsandnerds/xboxskins/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/noobsandnerds/xboxskins/raw/master/zips/addons.xml', 'repo_id' => 'repository.xboxskins', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xboxskins/repository.xboxskins-0.zip?raw=true' ),
		'helix' => array( 'name' => 'Official Kodi v14 Repo', 'dataUrl' => 'http://mirrors.xbmc.org/addons/helix/', 'xmlUrl' => 'http://mirrors.xbmc.org/addons/helix/addons.xml', 'statsUrl' => '',	'repo_id' => 'repository.xbmc.org', 'zip' => '1', 'downloadUrl' => ''),
		'gotham' => array( 'name' => 'Official XBMC v13 Repo', 'dataUrl' => 'http://mirrors.xbmc.org/addons/gotham/', 'xmlUrl' => 'http://mirrors.xbmc.org/addons/gotham/addons.xml', 'statsUrl' => '', 'repo_id' => 'repository.xbmc.org', 'zip' => '1', 'downloadUrl' => ''),
		'frodo' => array( 'name' => 'Official XBMC v12 Repo', 'dataUrl' => 'http://mirrors.xbmc.org/addons/frodo/', 'xmlUrl' => 'http://mirrors.xbmc.org/addons/frodo/addons.xml', 'statsUrl' => '', 'repo_id' => 'repository.xbmc.org', 'zip' => '1', 'downloadUrl' => ''),
	    'tvaddons' => array( 'name' => 'TVADDONS.ag Addon Repository', 'dataUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/', 'xmlUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/addons.xml', 'repo_id' => 'repository.xbmchub', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.6.zip'),
	    'tvaddons_common' => array( 'name' => 'TVADDONS.ag Libraries Repository', 'dataUrl' => 'https://offshoregit.com/tvaresolvers/tva-common-repository/raw/master/zips/', 'xmlUrl' => 'https://offshoregit.com/tvaresolvers/tva-common-repository/raw/master/addons.xml', 'repo_id' => 'repository.tva.common', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.6.zip'),
		'aaa_stream' => array ( 'name' => 'AAA Repository', 'dataUrl' => 'http://aaarepo.xyz/repo/zips/','statsUrl' => '', 'xmlUrl' => 'http://aaarepo.xyz/repo/addons.xml', 'repo_id' => 'repository.aaarepo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.aaarepo/repository.aaarepo-0.zip?raw=true' ),
		'abultman' => array( 'name' => 'Magnetism Repo', 'dataUrl' => 'http://raw.github.com/bultje76.addon.repository/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/abultman/bultje76.addon.repository/master/addons.xml', 'repo_id' => 'bultje76.addon.repository', 'zip' => '1', 'downloadUrl' => '' ), 
		'achilles' => array ( 'name' => 'achilles addons', 'dataUrl' => 'http://achilles-projects.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://achilles-projects.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.googlecode.achilles-projects', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.googlecode.achilles-projects/repository.googlecode.achilles-projects-0.zip?raw=true' ),
		'acv914' => array( 'name' => 'acv914 Add-ons', 'dataUrl' => 'http://acv914-xbmc.googlecode.com/git/', 'statsUrl' => '', 'xmlUrl' => 'http://acv914-xbmc.googlecode.com/git/addons.xml', 'repo_id' => 'repository.acv914.xbmc.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/alexisv/acv914-repo/raw/master/xbmc-repo/repository.acv914.xbmc.addons.zip' ), 
		'AddonBrasil' => array ( 'name' => 'AddonBrasil Repository', 'dataUrl' => 'http://raw.github.com/addonBrasil/addonBrasil-kodi/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/addonBrasil/addonBrasil-kodi/master/addons.xml', 'repo_id' => 'repository.addonBrasil', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.addonBrasil/repository.addonBrasil-0.zip?raw=true' ),
		'addons4xbox' => array( 'name' => 'addons4xbox repo', 'dataUrl' => 'https://github.com/xbmc4xbox/addons4xbox/raw/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/xbmc4xbox/addons4xbox/master/addons.xml', 'repo_id' => 'repository.addons4xbox', 'zip' => '1', 'downloadUrl' => '' ), 
		'AddonScriptorDE' => array( 'name' => 'AddonScriptorDE\'s Testing Repo', 'dataUrl' => 'http://addonscriptorde-beta-repo.googlecode.com/svn/trunk/', 'statsUrl' => '', 'xmlUrl' => 'http://addonscriptorde-beta-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.addonscriptorde-beta', 'zip' => '0', 'downloadUrl' => 'https://addonscriptorde-beta-repo.googlecode.com/files/repository.addonscriptorde-beta.zip' ),
		'AdrXbmc' => array ( 'name' => 'AMObox repository', 'dataUrl' => 'http://raw.github.com/adrxbmc/amobox.repository/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/adrxbmc/amobox.repository/master/addons.xml', 'repo_id' => 'amobox.repository', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/amobox.repository/amobox.repository-0.zip?raw=true' ),
		'AdultXBMC.com' => array( 'name' => 'AdultXBMC.com Add-on Repo', 'dataUrl' => 'https://offshoregit.com/adultxbmc/raw/master/', 'statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/adultxbmc/raw/master/addons.xml', 'repo_id' => 'repository.xxxadultxbmc', 'zip' => '', 'downloadUrl' => 'https://offshoregit.com/adultxbmc/raw/master/repository.xxxadultxbmc/repository.xxxadultxbmc-1.0.0.zip' ),
		'agx' => array( 'name' => 'agx\'s repo', 'dataUrl' => 'https://raw.githubusercontent.com/antigenx/xbmc-repo-agx/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/antigenx/xbmc-repo-agx/master/addons.xml', 'repo_id' => 'repository.xbmc-repo-agx', 'zip' => '1', 'downloadUrl' => 'https://github.com/antigenx/xbmc-repo-agx/blob/master/repository.xbmc-repo-agx/repository.xbmc-repo-agx-1.0.3.zip?raw=true' ), 
		'AH' => array( 'name' => 'AH Add-on repository', 'dataUrl' => 'https://raw.githubusercontent.com/addonhacker/ah-repo/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/addonhacker/ah-repo/master/addons.xml', 'repo_id' => 'repository.ah', 'zip' => '1', 'downloadUrl' => 'http://lvtvv.com/repo/repository.ah.zip' ), 
		'AJ' => array( 'name' => 'AJ Video Add-ons', 'dataUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.apple-tv2-xbmc', 'zip' => '0', 'downloadUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/addons/repository.googlecode.apple-tv2-xbmc/repository.googlecode.apple-tv2-xbmc-1.5.3.zip'), 
		'AJNewLook' => array( 'name' => 'AJ New Look Add-ons', 'dataUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/AddonsNewLookRepo/','statsUrl' => '', 'xmlUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/AddonsNewLookRepo/addons.xml', 'repo_id' => 'repository.aj-addons', 'zip' => '1', 'downloadUrl' => 'http://apple-tv2-xbmc.googlecode.com/svn/trunk/AddonsNewLookRepo/repository.aj-addons/repository.aj-addons-1.0.1.zip'), 
		'amitkeret' => array ( 'name' => 'amitkeret XBMC Add-ons', 'dataUrl' => 'https://raw.github.com/amitkeret/repository.amitkeret.xbmc/master/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/amitkeret/repository.amitkeret.xbmc/master/addons.xml', 'repo_id' => 'repository.amitkeret.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.amitkeret.xbmc/repository.amitkeret.xbmc-0.zip?raw=true' ),
		'AmpedAndWired' => array ( 'name' => 'Ampedandwired\'s XBMC Addons', 'dataUrl' => 'https://github.com/ampedandwired/ampedandwired-xbmc-repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/ampedandwired/ampedandwired-xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.ampedandwired', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.ampedandwired/repository.ampedandwired-0.zip?raw=true' ),
		'anarchintosh' => array( 'name' => 'anarchintosh Repo', 'dataUrl' => 'http://anarchintosh-projects.googlecode.com/svn/addons/', 'statsUrl' => '', 'xmlUrl' => 'http://anarchintosh-projects.googlecode.com/svn/addons/addons.xml', 'repo_id' =>  'repository.googlecode.anarchintosh-projects', 'zip' => '1', 'downloadUrl' => 'https://anarchintosh-projects.googlecode.com/files/repository.googlecode.anarchintosh-projects.1.0.1.zip' ), 
		'angelscry' => array( 'name' => 'Angelscry Add-ons', 'dataUrl' => 'http://www.gwenael.org/Repository/', 'statsUrl' => '', 'xmlUrl' => 'http://www.gwenael.org/Repository/addons.xml', 'repo_id' => 'repository.angelscry.xbmc-plugins', 'zip' => '1', 'downloadUrl' => 'http://www.gwenael.org/Repository/repository.angelscry.xbmc-plugins/repository.angelscry.xbmc-plugins-1.2.6.zip' ), 
		'anilkuj' => array( 'name' => 'anilkuj add-on repository', 'dataUrl' => 'https://github.com/anilkuj/xbmc-addons/raw/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'https://github.com/anilkuj/xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.github.anilkuj-xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/anilkuj/xbmc-addons/blob/master/repo/repository.github.anilkuj-xbmc-addons/repository.github.anilkuj-xbmc-addons-1.0.1.zip?raw=true' ), 
		'anonymous' => array ( 'name' => 'anonymous repo', 'dataUrl' => 'https://anonymousrepo.svn.codeplex.com/svn/anonymous-repo/','statsUrl' => '', 'xmlUrl' => 'https://anonymousrepo.svn.codeplex.com/svn/anonymous-repo/addons.xml', 'repo_id' => 'repository.anonymous', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.anonymous/repository.anonymous-0.zip?raw=true' ),
		'AnonymousAdult' => array( 'name' => 'Anonymous Adult Repo', 'dataUrl' => 'http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo-adults/', 'statsUrl' => '', 'xmlUrl' => 'http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo-adults/addons.xml', 'repo_id' => 'repository.anonymous.adults', 'zip' => '', 'downloadUrl' => 'https://anonymous-repo.googlecode.com/svn/trunk/repository.anonymous.adults.zip' ), 
		'anteo' => array ( 'name' => 'Anteo\'s Add-on Repository', 'dataUrl' => 'https://raw.githubusercontent.com/anteo/xbmc.repository/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/anteo/xbmc.repository/master/addons.xml', 'repo_id' => 'repository.anteo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.anteo/repository.anteo-0.zip?raw=true' ),
		'AznKodi' => array ( 'name' => 'AznKodi', 'dataUrl' => 'https://github.com/AznKodi/repository.AznKodi/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/AznKodi/repository.AznKodi/raw/master/addons.xml', 'repo_id' => 'repository.AznKodi', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.AznKodi/repository.AznKodi-0.zip?raw=true' ),
		'ao' => array( 'name' => 'ao Add-on Repository', 'dataUrl' => 'http://ao-xbmc-repository.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://ao-xbmc-repository.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.ao.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://ao-xbmc-repository.googlecode.com/files/repository.ao.xbmc-plugins.zip' ), 
#		'arabic-hadynz' => array( 'name' => 'Arabic Addons', 'dataUrl' => 'https://raw.githubusercontent.com/hadynz/repository.arabic.xbmc-addons/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'https://github.com/hadynz/repository.arabic.xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.arabic.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://dl.dropboxusercontent.com/s/udvtswqpb0hhgil/repository.arabic.xbmc-addons.zip?dl=1&token_hash=AAHoNqwhATpiP-LhUDTB3O4IsC2ckT0LuVOMoS6uW3zW2A' ), 
		'arabic-hadynz' => array ( 'name' => 'Arabic XBMC Add-on Repository', 'dataUrl' => 'https://raw.github.com/hadynz/repository.arabic.xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/hadynz/repository.arabic.xbmc-addons/master/addons.xml', 'repo_id' => 'repository.arabic.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.arabic.xbmc-addons/repository.arabic.xbmc-addons-0.zip?raw=true' ),
		'arb' => array ( 'name' => 'ARB Repo', 'dataUrl' => 'https://raw.githubusercontent.com/Andrewrb84/ARBMODRAPIER/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/Andrewrb84/ARBMODRAPIER/master/addons.xml', 'repo_id' => 'repository.arb', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.arb/repository.arb-0.zip?raw=true' ),
		'AudioDSP' => array( 'name' => 'Achim\'s Audio DSP repository', 'dataUrl' => 'https://raw.githubusercontent.com/AchimTuran/kodi-adsp-addons-repo/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/AchimTuran/kodi-adsp-addons-repo/master/addons.xml', 'repo_id' => 'repository.audiodsp.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/AchimTuran/kodi-adsp-addons-repo-dev/blob/master/repository.adsp.addons/repository.adsp.addons-0.0.1.zip?raw=true' ), 
		'avalonprojects.net' => array( 'name' => 'avalonprojects.net repository', 'dataUrl' => 'http://www.avalonprojects.net/xbmc/Repository/', 'statsUrl' => '', 'xmlUrl' => 'http://www.avalonprojects.net/xbmc/addons.xml', 'repo_id' => 'repository.avalonprojects', 'zip' => '1', 'downloadUrl' => 'https://github.com/avalonprojects/xbmc/blob/master/Repository/repository.avalonprojects/repository.avalonprojects-1.0.0.zip?raw=true' ), 
		'BancaDeJornais' => array( 'name' => 'Banca de Jornais Portugese Repo', 'dataUrl' => 'http://plugin-image-bancadejornais.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://plugin-image-bancadejornais.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.BancadeJornais.xbmc', 'zip' => '', 'downloadUrl' => 'https://plugin-image-bancadejornais.googlecode.com/files/repository.BancadeJornais.xbmc.zip' ), 
#		'Bas Rieter' => array( 'name' => 'XBMC Online TV (formerly XOT-Uzg.v3) Add-ons', 'dataUrl' => 'http://www.rieter.net/net.rieter.xot.repository/','statsUrl' => '', 'xmlUrl' => 'http://www.rieter.net/net.rieter.xot.www/addons.xml', 'repo_id' => 'net.rieter.xot.repository', 'zip' => '1', 'downloadUrl' => 'http://www.rieter.net/ext/?uri=http://xot.hamans.com/net.rieter.xot.repository-1.0.4.zip' ), 
		'Bas Rieter' => array ( 'name' => 'Retrospect (formerly XBMC Online TV) Add-ons', 'dataUrl' => 'http://www.rieter.net/net.rieter.xot.repository/','statsUrl' => '', 'xmlUrl' => 'http://www.rieter.net/net.rieter.xot.repository/addons.xml', 'repo_id' => 'net.rieter.xot.repository', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/net.rieter.xot.repository/net.rieter.xot.repository-0.zip?raw=true' ),
		'bbts' => array ( 'name' => 'BBTS Repo', 'dataUrl' => 'http://repo.bbtsip.tv/repo/addons/','statsUrl' => '', 'xmlUrl' => 'http://repo.bbtsip.tv/repo/addons.xml', 'repo_id' => 'repository.bbtsip.tv', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.bbtsip.tv/repository.bbtsip.tv-0.zip?raw=true' ),
		'beam' => array ( 'name' => 'Beam XBMC Add-ons', 'dataUrl' => 'http://xbmc-repo.bimovi.cz/packages/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-repo.bimovi.cz/addons.xml', 'repo_id' => 'repository.beam.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.beam.xbmc-addons/repository.beam.xbmc-addons-0.zip?raw=true' ),
		'bgaddons' => array ( 'name' => 'Bg Add-ons', 'dataUrl' => 'https://github.com/kodi1/kodi1.github.io/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/kodi1/kodi1.github.io/raw/master/repo/addons.xml', 'repo_id' => 'repo.bg.plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repo.bg.plugins/repo.bg.plugins-0.zip?raw=true' ),
		'bigbax' => array ( 'name' => 'XBMC.ru forum Add-ons', 'dataUrl' => 'https://github.com/xbmcrepo/ru/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/xbmcrepo/ru/raw/master/addons.xml', 'repo_id' => 'xbmcrepo.ru', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmcrepo.ru/xbmcrepo.ru-0.zip?raw=true' ),
// backup repo		'bigbax' => array ( 'name' => 'XBMC.ru forum Add-ons', 'dataUrl' => 'https://github.com/xbmcrus/XBMC.ru-forum-Add-ons/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/xbmcrus/XBMC.ru-forum-Add-ons/raw/master/addons.xml', 'repo_id' => 'repository.ru', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.ru/repository.ru-0.zip?raw=true' ),
		'bigsale' => array( 'name' => 'bigSale Add-on Repository', 'dataUrl' => 'http://bigsale-repository.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://bigsale-repository.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.bigsale', 'zip' => '', 'downloadUrl' => 'https://bigsale-repository.googlecode.com/files/repository.bigsale.zip' ), 
		'bisha' => array( 'name' => 'Bisha Arabic Addons', 'dataUrl' => 'https://github.com/bisha77/repository.arabic.xbmc-addons/raw/master/repo', 'statsUrl' => '', 'xmlUrl' => 'https://github.com/bisha77/repository.arabic.xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.arabic.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://dl.dropboxusercontent.com/s/udvtswqpb0hhgil/repository.arabic.xbmc-addons.zip?dl=1&token_hash=AAHoNqwhATpiP-LhUDTB3O4IsC2ckT0LuVOMoS6uW3zW2A' ), 
		'blacks' => array( 'name' => 'Black\'s Repo', 'dataUrl' => 'http://xperience1080.googlecode.com/svn/trunk/', 'statsUrl' => '', 'xmlUrl' => 'http://xperience1080.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.blacks', 'zip' => '1', 'downloadUrl' => 'https://xperience1080.googlecode.com/svn/trunk/repository.blacks.zip' ), 
		'blazetamer' => array( 'name' => 'BlazeTamer Repo', 'dataUrl' => 'http://offshoregit.com/Blazetamer/repo/raw/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/Blazetamer/repo/raw/master/addons.xml', 'repo_id' => 'repository.BlazeRepo', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo/repository.BlazeRepo-3.0.zip' ),
		'bluecop' => array( 'name' => 'Bluecop\'s Repo', 'dataUrl' => 'http://bluecop-xbmc-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://bluecop-xbmc-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.bluecop.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://bluecop-xbmc-repo.googlecode.com/files/repository.bluecop.xbmc-plugins.zip' ), 
		'bogs' => array ( 'name' => 'Bog\'s Addons', 'dataUrl' => 'http://bogs-xbmc-addons.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://bogs-xbmc-addons.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.googlecode.bogs-xbmc-addons', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.googlecode.bogs-xbmc-addons/repository.googlecode.bogs-xbmc-addons-0.zip?raw=true' ),
		'boogie' => array( 'name' => 'Boogie\'s Kodi Repo', 'dataUrl' => 'https://offshoregit.com/boogiepop/repository.boogie.dist/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/boogiepop/repository.boogie.dist/addons.xml', 'repo_id' => 'repository.boogie', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/boogiepop/repository.boogie.dist/repository.boogie/repository.boogie-0.0.7.zip' ), 
		'bossanova808' => array ( 'name' => 'bossanova808\'s XBMC Addons', 'dataUrl' => 'http://raw.github.com/bossanova808/repository.bossanova808/master/repository-downloads/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/bossanova808/repository.bossanova808/master/staging/addons.xml', 'repo_id' => 'repository.bossanova808', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.bossanova808/repository.bossanova808-0.zip?raw=true' ),
		'brazilian' => array ( 'name' => 'Brazilian XBMC Add-On Repository', 'dataUrl' => 'https://github.com/vitorhirota/repository.brazilian.xbmc-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/vitorhirota/repository.brazilian.xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.brazilian.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.brazilian.xbmc-addons/repository.brazilian.xbmc-addons-0.zip?raw=true' ),
		'brazzers' => array( 'name' => 'Brazzers-addon-repository', 'dataUrl' => 'http://github.com/slashing/kodi-brazzers/raw/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'http://github.com/slashing/kodi-brazzers/raw/master/addons.xml', 'repo_id' => 'repository.slashing', 'zip' => '1', 'downloadUrl' => 'https://github.com/slashing/kodi-brazzers/blob/master/repo/repository.slashing/repository.slashing-1.0.2.zip?raw=true' ), 
		'bromix' => array ( 'name' => 'Bromix Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/bromix/repository.bromix.storage/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/bromix/repository.bromix.storage/raw/master/addons.xml', 'repo_id' => 'repository.bromix', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.bromix/repository.bromix-0.zip?raw=true' ),
		'bstrdsmkr' => array( 'name' => 'bstrdsmkr\'s Repo', 'dataUrl' => 'http://repo.gosub.dk/bstrdsmkr/repo/','statsUrl' => '', 'xmlUrl' => 'http://repo.gosub.dk/bstrdsmkr/repository/addons.xml', 'repo_id' => 'repository.bstrdsmkr', 'zip' => '1', 'downloadUrl' => 'http://repo.gosub.dk/bstrdsmkr/repo/repository.bstrdsmkr/repository.bstrdsmkr-0.0.3.zip' ),
		'bunkford' => array( 'name' => 'bunkford Repo', 'dataUrl' => 'http://github.com/bunkford/Bunkford/raw/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'http://github.com/bunkford/Bunkford/raw/master/addons.xml', 'repo_id' => 'repository.bunkford', 'zip' => '1', 'downloadUrl' => 'https://github.com/bunkford/Bunkford/blob/master/zips/repository.bunkford/repository.bunkford-1.1.zip?raw=true' ), 
		'butchabay' => array( 'name' => 'repository butchabay', 'dataUrl' => 'http://xbmc-repository-butchabay.googlecode.com/svn/trunk/', 'statsUrl' => '', 'xmlUrl' => 'http://xbmc-repository-butchabay.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'xbmc.repo.butchabay', 'zip' => '1', 'downloadUrl' => 'https://xbmc-repository-butchabay.googlecode.com/files/xbmc.repo.butchabay.zip' ), 
		'byalongshot' => array( 'name' => 'ByALongShot\'s XBMC Addons', 'dataUrl' => 'http://andrewovens.com/xbmc/addons/', 'statsUrl' => '', 'xmlUrl' => 'http://andrewovens.com/xbmc/addons/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
		'CanadaOnDemand' => array( 'name' => 'marius-muja\'s fork of Andrepl\'s', 'dataUrl' => 'https://raw.github.com/irfancharania/canada.on.demand.repo/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/irfancharania/canada.on.demand.repo/master/addons.xml', 'repo_id' => 'repository.CanadaOnDemand', 'zip' => '1', 'downloadUrl' => 'https://github.com/irfancharania/canada.on.demand.repo/blob/master/zips/repository.CanadaOnDemand/repository.CanadaOnDemand-1.1.0.zip?raw=true' ), 
		'CanalPanda' => array( 'name' => 'CanalPanda.PT Repo', 'dataUrl' => 'http://plugin-video-canalpanda-xbmc.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://plugin-video-canalpanda-xbmc.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.canalpanda.xbmc', 'zip' => '', 'downloadUrl' => 'https://plugin-video-canalpanda-xbmc.googlecode.com/files/repository.canalpanda.xbmc.zip' ), 
		'ceth606' => array( 'name' => 'Ceth606\'s Add-on Repository', 'dataUrl' => 'https://github.com/Ceth606/xbmc-repo-ceth606/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/Ceth606/xbmc-repo-ceth606/master/addons.xml', 'repo_id' => 'xbmc-repo-ceth606', 'zip' => '', 'downloadUrl' => '' ), 
		'chakravyu' => array ( 'name' => 'Chakravyu\'s XBMC Addons', 'dataUrl' => 'https://github.com/chakravyu/repository.xbmc.chakra/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/chakravyu/repository.xbmc.chakra/raw/master/addons.xml', 'repo_id' => 'repository.xbmc.chakra', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xbmc.chakra/repository.xbmc.chakra-0.zip?raw=true' ),
		'chinese-tube' => array( 'name' => 'Addons for Chinese TV on Youtube', 'dataUrl' => 'http://xbmc-chinese-tube.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-chinese-tube.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.xbmc-chinese-tube', 'zip' => '', 'downloadUrl' => 'https://xbmc-chinese-tube.googlecode.com/files/repository.xbmc-chinese-tube.zip' ), 
		'chintogtokh' => array( 'name' => 'Chintogtokh XBMC Addon Repository', 'dataUrl' => 'https://raw.githubusercontent.com/chintogtokh/repository.chintogtokh.xbmc/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/chintogtokh/repository.chintogtokh.xbmc/master/addons.xml', 'repo_id' => 'repository.chintogtokh.xbmc', 'zip' => '1', 'downloadUrl' => '' ), 
		'claymic' => array( 'name' => 'Repo Claymic', 'dataUrl' => 'http://script-allinone.googlecode.com/svn/trunk/', 'statsUrl' => '', 'xmlUrl' => 'http://script-allinone.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.claymic', 'zip' => '1', 'downloadUrl' => 'https://mod-skin.googlecode.com/files/repository.claymic-1.0.1.zip' ), 
		'clubtv' => array( 'name' => 'Club TV Repository', 'dataUrl' => 'http://clubtv.dooremolen.com/addons/', 'statsUrl' => '', 'xmlUrl' => 'http://clubtv.dooremolen.com/addons/addons.xml', 'repo_id' => 'repository.clubtv.nl', 'zip' => '1', 'downloadUrl' => 'http://clubtv.dooremolen.com/addons/repository.clubtv.nl/repository.clubtv.nl-1.0.1.zip' ), 
		'cocawe' => array ( 'name' => 'Cocawe\'s REPO', 'dataUrl' => 'https://raw.github.com/cocawe/My-xbmc-repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/cocawe/My-xbmc-repo/master/addons.xml', 'repo_id' => 'repository.cocawe', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.cocawe/repository.cocawe-0.zip?raw=true' ),
		'codenx' => array( 'name' => 'codenx XBMC Addon Repository', 'dataUrl' => 'https://github.com/codenx/codenx-xbmc-addons/raw/master/data/', 'statsUrl' => '', 'xmlUrl' => 'https://github.com/codenx/codenx-xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.codenx.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/codenx/codenx-xbmc-addons/blob/master/repository.codenx.addons-2.2.1.zip?raw=true' ), 
		'const' => array ( 'name' => 'Const Kodi Add-ons', 'dataUrl' => 'https://github.com/const586/const-kodi-repo/raw/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://github.com/const586/const-kodi-repo/raw/master/addons/addons.xml', 'repo_id' => 'repository.const', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.const/repository.const-0.zip?raw=true' ),
		'coolwave' => array( 'name' => 'Coolwave\'s Addon Repository', 'dataUrl' => 'http://github.com/Coolwave/repository.Coolwave.v2/raw/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'http://github.com/Coolwave/repository.Coolwave.v2/raw/master/addons.xml', 'repo_id' => 'repository.Coolwave.v2', 'zip' => '1', 'downloadUrl' => '' ), 
		'coolwavebeta' => array ( 'name' => 'Coolwave beta Repo', 'dataUrl' => 'http://github.com/Coolwave/repository.betaCoolwave/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://github.com/Coolwave/repository.betaCoolwave/raw/master/addons.xml', 'repo_id' => 'repository.betaCoolwave', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.betaCoolwave/repository.betaCoolwave-0.zip?raw=true' ),
		'core-module-beta' => array( 'name' => 'Core Module Beta Testing Repo', 'dataUrl' => 'http://raw.github.com/Eldorados/Core-Module-Beta-Repo/master/repo/', 'statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Eldorados/Core-Module-Beta-Repo/master/addons.xml', 'repo_id' => 'repository.coremodule.betas', 'zip' => '1', 'downloadUrl' => 'https://github.com/Eldorados/Core-Module-Beta-Repo/blob/master/repo/repository.coremodule.betas/repository.coremodule.betas-1.0.0.zip?raw=true' ), 
		'crzen' => array( 'name' => 'Crzen\'s Repository', 'dataUrl' => 'http://raw.github.com/crzen/repository.crzen/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/crzen/repository.crzen/master/addons.xml', 'repo_id' => 'repository.crzen', 'zip' => '1', 'downloadUrl' => 'https://github.com/crzen/repository.crzen/blob/master/zips/repository.crzen/repository.crzen-0.1.0.zip?raw=true' ), 
		'cubicle-vdo' => array ( 'name' => 'XBMC Israeli Streaming Sites Repo', 'dataUrl' => 'https://raw.githubusercontent.com/cubicle-vdo/xbmc-israel/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/cubicle-vdo/xbmc-israel/master/addons.xml', 'repo_id' => 'repository.xbmc-israel', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xbmc-israel/repository.xbmc-israel-0.zip?raw=true' ),
		'cycnow' => array( 'name' => 'xbmc-cycnow Add-on Repository', 'dataUrl' => 'http://repo.xbmc-cycnow.googlecode.com/hg/', 'statsUrl' => '', 'xmlUrl' => 'http://repo.xbmc-cycnow.googlecode.com/hg/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-cycnow', 'zip' => '1', 'downloadUrl' => 'http://repo.xbmc-cycnow.googlecode.com/hg/repository.googlecode.xbmc-cycnow/repository.googlecode.xbmc-cycnow-latest.zip' ), 
		'cyrus007' => array ( 'name' => 'Cyrus007 addons', 'dataUrl' => 'https://github.com/cyrus007/xbmc-addons/raw/master/repository.cyrus007/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/cyrus007/xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.github.cyrus007-xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.github.cyrus007-xbmc-addons/repository.github.cyrus007-xbmc-addons-0.zip?raw=true' ),
		'd0f21' => array ( 'name' => 'd0f21\'s XBMC Addons', 'dataUrl' => 'https://github.com/louca1221/d0f21-Repository/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/louca1221/d0f21-Repository/master/addons.xml', 'repo_id' => 'repository.d0f21', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.d0f21/repository.d0f21-0.zip?raw=true' ),
		'dandar3' => array( 'name' => 'Dandar3 Add-ons', 'dataUrl' => 'http://dandar3-xbmc-addons.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://dandar3-xbmc-addons.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.dandar3-xbmc-addons', 'zip' => '', 'downloadUrl' => 'https://dandar3-xbmc-addons.googlecode.com/files/repository.googlecode.dandar3-xbmc-addons.zip' ), 
		'Dany' => array ( 'name' => 'Source OFFICIELLE de plugins Infologique.net', 'dataUrl' => 'http://tv.infologique.net/XBMC/zip/','statsUrl' => '', 'xmlUrl' => 'http://tv.infologique.net/XBMC/addons.xml', 'repo_id' => 'repository.infologiqueTV', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.infologiqueTV/repository.infologiqueTV-0.zip?raw=true' ),
		'Datho-Digital' => array ( 'name' => 'Datho Add-on Repository', 'dataUrl' => 'http://raw.github.com/datho/datho-xbmc-repo/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/datho/datho-xbmc-repo/master/addons.xml', 'repo_id' => 'repository.datho.xbmc-plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.datho.xbmc-plugins/repository.datho.xbmc-plugins-0.zip?raw=true' ),
		'dss' => array( 'name' => 'Dutch Sports Streams Repository', 'dataUrl' => 'https://raw.githubusercontent.com/dutchsportstreams/DSS/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/dutchsportstreams/DSS/master/addons.xml', 'repo_id' => 'repository.dss', 'zip' => '1', 'downloadUrl' => 'https://github.com/dutchsportstreams/DSS/blob/master/repo/repository.dss/repository.dss-1.2.zip?raw=true' ), 
		'dbsr' => array ( 'name' => 'dbsrs xbmc addon repo', 'dataUrl' => 'https://github.com/dbsr/repository.dbsr.xbmc_addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/dbsr/repository.dbsr.xbmc_addons/raw/master/addons.xml', 'repo_id' => 'repository.dbsr.xbmc_addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.dbsr.xbmc_addons/repository.dbsr.xbmc_addons-0.zip?raw=true' ),
		'ddurdle' => array( 'name' => 'ddurdle\'s Cloud Services KODI XBMC Addons', 'dataUrl' => 'http://dmdsoftware.net/repository.ddurdle/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/ddurdle/repository.ddurdle/master/addons.xml', 'repo_id' => 'repository.ddurdle', 'zip' => '1', 'downloadUrl' => 'http://dmdsoftware.net/repository.ddurdle/repository.ddurdle.zip' ), 
		'DeusMaior' => array( 'name' => 'DeusMaior Repository', 'dataUrl' => 'http://pluginxbmctvi24.googlecode.com/svn/trunk/', 'statsUrl' => '', 'xmlUrl' => 'http://pluginxbmctvi24.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.tvi24.xbmc', 'zip' => '', 'downloadUrl' => 'http://xbmc.aminhacasadigital.com/1-Essenciais%20PT/repository.tvi24.xbmc.zip' ), 
		'dextertv' => array( 'name' => 'dextertv repo', 'dataUrl' => 'https://raw.githubusercontent.com/xoptimus/dexter/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/xoptimus/dexter/master/addons.xml', 'repo_id' => 'repository.dextertv', 'zip' => '1', 'downloadUrl' => 'http://dexteriptv.com/repo/repository.dextertv.zip' ), 
		'divingmule' => array( 'name' => 'Divingmule Add-ons', 'dataUrl' => 'http://divingmules-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://divingmules-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.divingmule.addons', 'zip' => '', 'downloadUrl' => 'https://divingmules-repo.googlecode.com/files/repository.divingmule.addons.zip' ), 
		'DixieDean' => array( 'name' => 'DixieDean Add-ons', 'dataUrl' => 'https://raw.github.com/DixieDean/Dixie-Deans-XBMC-Repo/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/DixieDean/Dixie-Deans-XBMC-Repo/master/addons.xml', 'repo_id' => 'repository.Dixie-Deans-XBMC-Repo', 'zip' => '1', 'downloadUrl' => 'https://github.com/DixieDean/Dixie-Deans-XBMC-Repo/blob/master/zips/repository.Dixie-Deans-XBMC-Repo/repository.Dixie-Deans-XBMC-Repo-1.0.8.zip?raw=true' ), 
		'dk' => array ( 'name' => 'The other Viet Addons', 'dataUrl' => 'https://bitbucket.org/dknlght/dk-xbmc-repaddon-rep/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://bitbucket.org/dknlght/dk-xbmc-repaddon-rep/raw/master/addons.xml', 'repo_id' => 'repository.otherguysstuff', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.otherguysstuff/repository.otherguysstuff-0.zip?raw=true' ),
		'dk-XBMC' => array ( 'name' => 'dk-xbmc Add-on Repository', 'dataUrl' => 'http://raw.githubusercontent.com/dknlght/dkodi/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.githubusercontent.com/dknlght/dkodi/master/addons.xml', 'repo_id' => 'repository.dk-xbmc-repaddon', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.dk-xbmc-repaddon/repository.dk-xbmc-repaddon-0.zip?raw=true' ),
		'DMD-Czech' => array( 'name' => 'DMD-XBMC Czech Add-ons', 'dataUrl' => 'http://dmd-xbmc.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://dmd-xbmc.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.dmd-xbmcv2.googlecode.com', 'zip' => '', 'downloadUrl' => 'https://dmd-xbmc.googlecode.com/files/repository.dmd-xbmcv2.googlecode.com.zip' ), 
		'docshadrach' => array( 'name' => 'Doc Shadrach\'s Add-ons', 'dataUrl' => 'http://github.com/XBMCSpot/docshadrach.repository/raw/master/zips/', 'statsUrl' => '', 'xmlUrl' => 'http://github.com/XBMCSpot/docshadrach.repository/raw/master/addons.xml', 'repo_id' => 'repository.docshadrach', 'zip' => '1', 'downloadUrl' => 'https://github.com/XBMCSpot/docshadrach.repository/blob/master/zips/repository.docshadrach/repository.docshadrach-1.0.zip?raw=true' ), 
		'dodoadoodoo' => array( 'name' => 'dodoadoodoo Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/dodoadoodoo/xbmc-repository/master/', 'statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/dodoadoodoo/xbmc-repository/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
		'doplnky' => array( 'name' => 'XBMC doplnky Czech', 'dataUrl' => 'http://lzoubek.github.io/xbmc-doplnky/repo/', 'statsUrl' => '', 'xmlUrl' => 'http://lzoubek.github.io/xbmc-doplnky/repo/addons.xml', 'repo_id' => 'repository.xbmc.doplnky', 'zip' => '1', 'downloadUrl' => 'http://lzoubek.github.io/xbmc-doplnky/repo/repository.xbmc.doplnky/repository.xbmc.doplnky-1.0.4.zip' ), 
		'drascom' => array( 'name' => 'drascom Add-on Repository', 'dataUrl' => 'https://xbmc-tr-team-turkish-addons.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'https://xbmc-tr-team-turkish-addons.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'xbmcTR.repo', 'zip' => '1', 'downloadUrl' => 'https://xbmc-tr-team-turkish-addons.googlecode.com/files/xbmcTR.repo-1.0.7.zip' ), 
		'drascom' => array ( 'name' => 'xbmcTR.repo', 'dataUrl' => 'https://github.com/koditr/xbmc-tr-team-turkish-addons/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/koditr/xbmc-tr-team-turkish-addons/raw/master/addons.xml', 'repo_id' => 'xbmcTR.repo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmcTR.repo/xbmcTR.repo-0.zip?raw=true' ),
		'drascom-scraper' => array( 'name' => 'Turkish Add-ons', 'dataUrl' => 'http://turkishxbmcscraper.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'https://turkishxbmcscraper.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'drascom.repo', 'zip' => '1', 'downloadUrl' => 'http://turkishxbmcscraper.googlecode.com/files/xbmcTR.repo_1.0.5.zip' ), 
		'DreamHD TECbox' => array ( 'name' => 'iVue TV Guide Add-on', 'dataUrl' => 'http://tecbox.tv/repo/teciptvguide/','statsUrl' => '', 'xmlUrl' => 'http://tecbox.tv/repo/teciptvguide/addons.xml', 'repo_id' => 'xbmc.repo.tecboxtvguide', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.tecboxtvguide/xbmc.repo.tecboxtvguide-0.zip?raw=true' ),
// Backup repo		'DreamHD TECbox' => array ( 'name' => 'iVue TV Guide Add-on', 'dataUrl' => 'https://raw.githubusercontent.com/totaltec2014/ivuerepo/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/totaltec2014/ivuerepo/master/addons.xml', 'repo_id' => 'xbmc.repo.tecboxtvguide', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.tecboxtvguide/xbmc.repo.tecboxtvguide-0.zip?raw=true' ),
		'DudeHere' => array ( 'name' => 'DudeHere Addons', 'dataUrl' => 'https://offshoregit.com/dudehere-repository/addons/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/dudehere-repository/addons/addons.xml', 'repo_id' => 'repository.dudehere.plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.dudehere.plugins/repository.dudehere.plugins-0.zip?raw=true' ),
		'dvor85' => array ( 'name' => 'dvor85 XBMC Add-ons', 'dataUrl' => 'https://github.com/dvor85/kodi.repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/dvor85/kodi.repo/raw/master/addons.xml', 'repo_id' => 'repository.dvor85', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.dvor85/repository.dvor85-0.zip?raw=true' ),
		'eldorado' => array ( 'name' => 'Eldorado\'s XBMC Addons', 'dataUrl' => 'http://raw.github.com/Eldorados/eldorado-xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Eldorados/eldorado-xbmc-addons/master/addons.xml', 'repo_id' => 'repository.eldorado', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.eldorado/repository.eldorado-0.zip?raw=true' ),
		'eldorado-core' => array ( 'name' => 'Core Module Beta Testing Repo', 'dataUrl' => 'https://github.com/Eldorados/Core-Module-Beta-Repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/Eldorados/Core-Module-Beta-Repo/raw/master/addons.xml', 'repo_id' => 'repository.coremodule.betas', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.coremodule.betas/repository.coremodule.betas-0.zip?raw=true' ),
		'eleazar' => array( 'name' => 'eleazar Repo', 'dataUrl' => 'https://offshoregit.com/eleazarcoding/eleazar-xbmc/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/eleazarcoding/eleazar-xbmc/raw/master/addons.xml', 'repo_id' => 'repository.eleazar', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/eleazarcoding/eleazar-xbmc/raw/master/repository.eleazar/repository.eleazar-1.3.zip' ), 
		'elmerohueso' => array( 'name' => 'elmerohueso\'s Add-on Repository', 'dataUrl' => 'https://github.com/elmerohueso/xbmc.repo.elmerohueso/raw/master/download/','statsUrl' => '', 'xmlUrl' => 'http://github.com/elmerohueso/xbmc.repo.elmerohueso/raw/master/download/addons.xml', 'repo_id' => 'xbmc.repo.elmerohueso', 'zip' => '1', 'downloadUrl' => 'https://github.com/elmerohueso/xbmc.repo.elmerohueso/blob/master/download/xbmc.repo.elmerohueso/xbmc.repo.elmerohueso-1.0.zip?raw=true' ), 
		'entertainment' => array( 'name' => 'The Entertainment Repository', 'dataUrl' => 'https://raw.github.com/MrEntertainment/EntertainmentREPO/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/MrEntertainment/EntertainmentREPO/master/addons.xml', 'repo_id' => 'repository.entertainmentrepo', 'zip' => '1', 'downloadUrl' => 'https://github.com/MrEntertainment/EntertainmentREPO/raw/master/zips/repository.entertainmentrepo/repository.entertainmentrepo-1.1.zip' ), 
		'eugenebond' => array( 'name' => 'Eugene Bond XBMC Add-ons', 'dataUrl' => 'https://github.com/Eugene-Bond/xmbc-plugins/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/Eugene-Bond/xmbc-plugins/raw/master/addons.xml', 'repo_id' => 'repository.bond', 'zip' => '1', 'downloadUrl' => 'https://github.com/Eugene-Bond/xmbc-plugins/blob/master/repository.bond/repository.bond-1.0.1.zip?raw=true' ), 
		'evgen-dev' => array( 'name' => 'Evgen_dev XBMC Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/evgen-dev/repository.evgen_dev.xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/evgen-dev/repository.evgen_dev.xbmc-addons/master/addons.xml', 'repo_id' => 'repository.evgen_dev', 'zip' => '1', 'downloadUrl' => 'https://github.com/evgen-dev/repository.evgen_dev.xbmc-addons/blob/master/repository.evgen_dev.zip?raw=true' ), 
		'eyal' => array( 'name' => 'Eyal TV Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/Eyal87/repository.eyal/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/Eyal87/repository.eyal/master/addons.xml', 'repo_id' => 'repository.eyal', 'zip' => '1', 'downloadUrl' => 'https://github.com/Eyal87/repository.eyal/blob/master/repository.eyal.zip?raw=true' ), 
 		'fastcolors' => array( 'name' => 'fastcolors Repo', 'dataUrl' => 'http://fastcolors.net/Repo/','statsUrl' => '', 'xmlUrl' => 'http://fastcolors.net/Repo/addons.xml', 'repo_id' => 'repository.fastcolors', 'zip' => '1', 'downloadUrl' => 'http://fastcolors.net/Repo/repository.fastcolors/repository.fastcolors-3.0.1.zip' ), 
		'fehmer' => array ( 'name' => 'Addons for deaf people', 'dataUrl' => 'https://raw.github.com/fehmer/xbmc-repository/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/fehmer/xbmc-repository/master/addons.xml', 'repo_id' => 'repository.github.fehmer', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.github.fehmer/repository.github.fehmer-0.zip?raw=true' ),
		'fightnight' => array( 'name' => 'J0anita Repo', 'dataUrl' => 'https://fightnightkodi.svn.codeplex.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'https://fightnightkodi.svn.codeplex.com/svn/addons/addons.xml', 'repo_id' => 'repository.fightnight', 'zip' => '1', 'downloadUrl' => 'https://fightnightkodi.svn.codeplex.com/svn/addons/repository.fightnight/repository.fightnight-1.5.zip' ), 
		'flopes' => array( 'name' => 'flopes Add-on Repository', 'dataUrl' => 'http://repo-flopes-xbmc.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://repo-flopes-xbmc.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.flopes.xbmc', 'zip' => '0', 'downloadUrl' => 'https://repo-flopes-xbmc.googlecode.com/svn/trunk/repository.flopes.xbmc.zip' ), 
		'francescosoft' => array ( 'name' => 'francescosoft\'s XBMC REPO', 'dataUrl' => 'http://github.com/francescosoft/openelec-addons/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://github.com/francescosoft/openelec-addons/raw/master/addons.xml', 'repo_id' => 'repository.openelec-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.openelec-addons/repository.openelec-addons-0.zip?raw=true' ),
		'freeman' => array ( 'name' => 'freem@n\'s Add-ons', 'dataUrl' => 'https://raw.github.com/freeman212/xbmc.repo.freeman/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/freeman212/xbmc.repo.freeman/master/addons.xml', 'repo_id' => 'xbmc.repo.freeman', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.freeman/xbmc.repo.freeman-0.zip?raw=true' ),
		'FTVGuideRepo' => array( 'name' => 'FTV Guide Repo', 'dataUrl' => 'http://raw.github.com/bluezed/FTV-Guide-Repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/bluezed/FTV-Guide-Repo/master/addons.xml', 'repo_id' => 'repository.FTV-Guide-Repo', 'zip' => '1', 'downloadUrl' => 'http://raw.github.com/bluezed/FTV-Guide-Repo/master/zips/repository.FTV-Guide-Repo/repository.FTV-Guide-Repo-1.1.zip' ),
		'gbzygil' => array( 'name' => 'gbzygil XBMC Addon Repository', 'dataUrl' => 'https://github.com/gbzygil/gbzygil-xbmc-repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/gbzygil/gbzygil-xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.gbzygil', 'zip' => '', 'downloadUrl' => 'https://github.com/gbzygil/gbzygil-xbmc-repo/blob/master/repository.gbzygil-IndianMovies.zip?raw=true' ), 
		'hal9000' => array( 'name' => 'HAL9000 Add-on Repository', 'dataUrl' => 'https://raw.githubusercontent.com/xbmc-addon/repository.hal9000/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/xbmc-addon/repository.hal9000/master/addons.xml', 'repo_id' => 'repository.hal9000', 'zip' => '1', 'downloadUrl' => 'https://github.com/xbmc-addon/repository.hal9000/blob/master/repository.hal9000.zip?raw=true' ), 
		'halow' => array( 'name' => 'Halow Repository', 'dataUrl' => 'https://raw.githubusercontent.com/HalowTV/Halowrepo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/HalowTV/Halowrepo/master/zips/addons.xml', 'repo_id' => 'repository.Halowrepo', 'zip' => '1', 'downloadUrl' => 'https://github.com/HalowTV/Halowrepo/blob/master/zips/repository.HalowRepo/repository.Halowrepo-1.6.0.zip?raw=true' ), 
		'Hashiname' => array( 'name' => 'Hashiname Add-on Repository', 'dataUrl' => 'https://raw.githubusercontent.com/hasherdene/kodi-repo-hashiname/master/datadir/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/hasherdene/kodi-repo-hashiname/master/addons.xml', 'repo_id' => 'repository.hashiname', 'zip' => '1', 'downloadUrl' => 'https://github.com/hasherdene/kodi-repo-hashiname/blob/master/datadir/repository.hashiname/repository.hashiname-0.2.zip?raw=true' ), 
		'Hc232' => array( 'name' => 'Asteron\'s Addon Repository', 'dataUrl' => 'http://github.com/Hc232/xbmc.repository/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/Hc232/xbmc.repository/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
		'HDPfans' => array ( 'name' => 'HDPfans Repo', 'dataUrl' => 'http://repo.tofuos.com/zips/','statsUrl' => '', 'xmlUrl' => 'http://repo.tofuos.com/addons.xml', 'repo_id' => 'repository.hdpfans.xbmc-addons-chinese', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.hdpfans.xbmc-addons-chinese/repository.hdpfans.xbmc-addons-chinese-0.zip?raw=true' ),
		'HEXbmcBrasil' => array( 'name' => 'HE Xbmc Brasil Repository', 'dataUrl' => 'http://he-repository-brasil.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://he-repository-brasil.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.he.xbmc', 'zip' => '0', 'downloadUrl' => 'https://he-repository-brasil.googlecode.com/svn/trunk/repository.xbmc-he-brasil.zip' ), 
		'hippojay' => array( 'name' => 'PlexBMC Add-on Repository', 'dataUrl' => 'http://hippojay.github.io/repository.plexbmc.addons/download/','statsUrl' => '', 'xmlUrl' => 'http://hippojay.github.io/repository.plexbmc.addons/download/addons.xml', 'repo_id' => 'repository.plexbmc.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/hippojay/repository.plexbmc.addons/blob/frodo/download/xbmc.repo.plexbmc/xbmc.repo.plexbmc-2.0.2.zip?raw=true' ), 
		'hippojay-frodo' => array ( 'name' => 'PleXBMC Add-ons for XBMC', 'dataUrl' => 'http://repository-plexbmc-addons.googlecode.com/git-history/frodo/download/','statsUrl' => '', 'xmlUrl' => 'http://repository-plexbmc-addons.googlecode.com/git-history/frodo/addons.xml', 'repo_id' => 'xbmc.repo.plexbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.plexbmc/xbmc.repo.plexbmc-0.zip?raw=true' ),
/*password protected */		'hitcher' => array( 'name' => 'Hitcher\'s  Add-on Repository', 'dataUrl' => 'http://hitcher-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://hitcher-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'xbmc.repo.hitcher', 'zip' => '1', 'downloadUrl' => 'http://hitcher-repo.googlecode.com/svn/trunk/xbmc.repo.hitcher/xbmc.repo.hitcher-5.0.0.zip' ), 
		'hmsb' => array ( 'name' => 'HMB Repository', 'dataUrl' => 'http://hmsb.github.io/repository.hmb.xbmc.addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/HMSB/repository.hmb.xbmc.addons/gh-pages/addons.xml', 'repo_id' => 'repository.hmb.xbmc.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.hmb.xbmc.addons/repository.hmb.xbmc.addons-0.zip?raw=true' ),
		'HTPC-Solutions' => array ( 'name' => 'HTPC Solutions Repository', 'dataUrl' => 'https://raw.github.com/htpcsolutions/downloads/master/kodi/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/htpcsolutions/downloads/master/kodi/addons.xml', 'repo_id' => 'repository.htpc-solutions', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.htpc-solutions/repository.htpc-solutions-0.zip?raw=true' ),
		'huball' => array ( 'name' => 'huball-repo', 'dataUrl' => 'http://xbmc-huball-repository.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-huball-repository.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.huball', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.huball/repository.huball-0.zip?raw=true' ),
		'humla' => array ( 'name' => 'humla Add-on Repository', 'dataUrl' => 'https://raw.githubusercontent.com/humla/canadanepal-xbmc/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/humla/canadanepal-xbmc/master/humla_repo/addons.xml', 'repo_id' => 'repository.humla', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.humla/repository.humla-0.zip?raw=true' ),
		'husham' => array( 'name' => 'Husham.com Repo', 'dataUrl' => 'https://raw.githubusercontent.com/hmemar/husham.com/master/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/hmemar/husham.com/master/repository/addons.xml', 'repo_id' => 'repository.husham.com', 'zip' => '1', 'downloadUrl' => 'https://github.com/hmemar/husham.com/blob/master/zip/repository.husham.com/repository.husham.com-1.1.0003.zip?raw=true' ), 
		'hybrid-development' => array( 'name' => 'Hybrid Development Repo', 'dataUrl' => 'http://hybrid-development-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://hybrid-development-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repo.hybrid', 'zip' => '1', 'downloadUrl' => 'http://hybrid-development-repo.googlecode.com/svn/trunk/xbmc.repo.hybrid/xbmc.repo.hybrid-1.0.0.zip' ), 
		'iamfreetofly' => array( 'name' => 'Iamfreetofly Add-ons', 'dataUrl' => 'https://raw.github.com/iamfreetofly/repository.iamfreetofly-xbmc-repaddon-bb/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/iamfreetofly/repository.iamfreetofly-xbmc-repaddon-bb/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
		'icanuck' => array( 'name' => 'iCanuck\'s Repo', 'dataUrl' => 'https://github.com/iCanuck/iCanuck-XBMC-Repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/iCanuck/iCanuck-XBMC-Repo/master/addons.xml', 'repo_id' => 'repository.icanuck', 'zip' => '1', 'downloadUrl' => 'https://github.com/iCanuck/iCanuck-XBMC-Repo/blob/master/repository.icanuck/repository.icanuck-1.0.zip?raw=true' ), 
		'icanuck-Kodi' => array ( 'name' => 'iCanuck\'s Kodi Repository', 'dataUrl' => 'http://offshoregit.com/iCanuck/iCanuck-Repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/iCanuck/iCanuck-Repo/raw/master/addons.xml', 'repo_id' => 'repository.icanuck', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.icanuck/repository.icanuck-0.zip?raw=true' ),
		'icharania' => array( 'name' => 'icharania Repo', 'dataUrl' => 'https://raw.github.com/irfancharania/icharania.repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/irfancharania/icharania.repo/master/addons.xml', 'repo_id' => 'repository.icharania', 'zip' => '1', 'downloadUrl' => 'https://github.com/irfancharania/canada.on.demand.repo/blob/master/zips/repository.CanadaOnDemand/repository.CanadaOnDemand-1.1.0.zip?raw=true' ), 
		'IPTV' => array( 'name' => 'IPTV Addons', 'dataUrl' => 'http://github.com/IICUX/xbmc-iptv-plugin/raw/master/xbmc_repo/','statsUrl' => '', 'xmlUrl' => 'http://github.com/IICUX/xbmc-iptv-plugin/raw/master/xbmc_repo/addons.xml', 'repo_id' => 'repository.iptv.plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/IICUX/xbmc-iptv-plugin/raw/master/repository.iptv.plugins.zip' ), 
		'IPTVxtra' => array( 'name' => 'IPTVxtra XBMC Add-on', 'dataUrl' => 'http://srv1.iptvxtra.net/xbmc/addons/','statsUrl' => '', 'xmlUrl' => 'http://srv1.iptvxtra.net/xbmc/addons/addons.xml', 'repo_id' => 'repository.iptvxtra', 'zip' => '1', 'downloadUrl' => 'http://www.iptvxtra.net/xbmc/addons/repository.iptvxtra.zip' ), 
		'IPTVxtra-kodi' => array ( 'name' => 'IPTVxtra KODI Add-ons', 'dataUrl' => 'http://srv1.iptvxtra.com/addons/','statsUrl' => '', 'xmlUrl' => 'http://srv1.iptvxtra.com/addons/addons.xml', 'repo_id' => 'repository.iptvxtra', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.iptvxtra/repository.iptvxtra-0.zip?raw=true' ),
		'IPTVxtra-movies' => array ( 'name' => 'IPTVxtra KODI Movie Add-ons', 'dataUrl' => 'http://srv1.iptvxtra.com/addons_movie/','statsUrl' => '', 'xmlUrl' => 'http://srv1.iptvxtra.com/addons_movie/addons.xml', 'repo_id' => 'repository.iptvxtra_movie', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.iptvxtra_movie/repository.iptvxtra_movie-0.zip?raw=true' ),
		'iStream' => array ( 'name' => 'iSTREAM XBMC Addons Repository', 'dataUrl' => 'http://istreamrepo.me/istream/repo/zips/','statsUrl' => '', 'xmlUrl' => 'http://istreamrepo.me/istream/repo/addons.xml', 'repo_id' => 'repository.istream', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.istream/repository.istream-0.zip?raw=true' ),
		'iWillFolo' => array( 'name' => 'iWillFolo add-ons', 'dataUrl' => 'http://iwillfolo.com/wordpress/wp-content/uploads/download_dir/','statsUrl' => '', 'xmlUrl' => 'http://iwillfolo.com/wordpress/wp-content/uploads/download_dir/addons.xml', 'repo_id' => 'repository.iWillFolo.xbmc', 'zip' => '1', 'downloadUrl' => 'http://iwillfolo.com/iwf/repository.iWillFolo.xbmc.zip' ), 
/*DNS Lookup Failed - site down */		'janlul' => array( 'name' => 'Dutch Sports Stream Repo', 'dataUrl' => 'http://repo.dooremolen.com/addons/repo/','statsUrl' => '', 'xmlUrl' => 'http://repo.dooremolen.com/addons/addons.xml', 'repo_id' => 'repository.repojanlul', 'zip' => '1', 'downloadUrl' => '' ), 
		'japanese' => array( 'name' => 'Japanese XBMC Add-ons', 'dataUrl' => 'https://raw.github.com/xbmc-now/japanese-xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/xbmc-now/japanese-xbmc-addons/master/repo/addons.xml', 'repo_id' => 'repository.japanese', 'zip' => '1', 'downloadUrl' => 'https://github.com/xbmc-now/japanese-xbmc-addons/blob/master/repo/repository.japanese/repository.japanese-1.0.0.zip?raw=true' ), 
// His repo is now conflicting with his old one - the prick		'Jas0nPCOriginal' => array( 'name' => 'Jas0nPC\'s Original Repo', 'dataUrl' => 'https://raw.github.com/jas0npc/jas0npc/master/zips/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => 'repository.jas0npc', 'zip' => '1', 'downloadUrl' => 'https://github.com/jas0npc/jas0npc/blob/master/zips/repository.Jas0npc/repository.Jas0npc-1.6.zip?raw=true' ), 
		'Jas0npcNEW' => array( 'name' => '__Jas0npc__ Repository', 'dataUrl' => 'http://raw.github.com/jas0npc/kodi/master/addons/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/jas0npc/kodi/master/addons/addons.xml', 'repo_id' => 'repository.jas0npc', 'zip' => '1', 'downloadUrl' => 'http://jas0npc.pcriot.com/repository.jas0npc-1.0.6.zip' ), 
		'jeroen' => array ( 'name' => 'Jeroen\'s Add-on Repository', 'dataUrl' => 'https://github.com/jeroenpardon/xbmc.repo.jeroen/raw/master/download/','statsUrl' => '', 'xmlUrl' => 'http://github.com/jeroenpardon/xbmc.repo.jeroen/raw/master/addons.xml', 'repo_id' => 'xbmc.repo.jeroen', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.jeroen/xbmc.repo.jeroen-0.zip?raw=true' ),
		'Joel' => array ( 'name' => 'Joel\'s LiveTV Repo', 'dataUrl' => 'https://raw.githubusercontent.com/joelgrace1/repository.livetv/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/joelgrace1/repository.livetv/master/addons.xml', 'repo_id' => 'repository.livetv', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.livetv/repository.livetv-0.zip?raw=true' ),
/* Site down */		'jools' => array( 'name' => 'Jools Repository', 'dataUrl' => 'http://cyco.se/xbmc/repo/','statsUrl' => '', 'xmlUrl' => 'http://cyco.se/xbmc/repository/addons.xml', 'repo_id' => 'repository.jools', 'zip' => '1', 'downloadUrl' => 'http://cyco.se/xbmc/repo/repository.jools/repository.jools-0.1.0.zip' ), 
		'Jugger' => array ( 'name' => 'Kodinerds Repo', 'dataUrl' => 'http://repo.skinquantum.de/nerdsrepo/kodi14/','statsUrl' => '', 'xmlUrl' => 'http://repo.skinquantum.de/nerdsrepo/kodi14/addons.xml', 'repo_id' => 'repository.kodinerds', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.kodinerds/repository.kodinerds-0.zip?raw=true' ),
		'k3oni' => array ( 'name' => 'K3oni\'s Addon Repository', 'dataUrl' => 'https://github.com/k3oni/repository.k3oni.xbmc-addons/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/k3oni/repository.k3oni.xbmc-addons/master/addons.xml', 'repo_id' => 'repository.k3oni.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.k3oni.xbmc/repository.k3oni.xbmc-0.zip?raw=true' ),
		'KAOSbox' => array ( 'name' => 'KAOSbox Repo', 'dataUrl' => 'http://repo.kaosbox.tv/zips/','statsUrl' => '', 'xmlUrl' => 'http://repo.kaosbox.tv/addons.xml', 'repo_id' => 'repository.kaosbox', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.kaosbox/repository.kaosbox-0.zip?raw=true' ),
		'KAOSboxHelix' => array ( 'name' => 'New KAOSbox Repo', 'dataUrl' => 'http://repobox.kaosbox.tv/zips/','statsUrl' => '', 'xmlUrl' => 'http://repobox.kaosbox.tv/addons.xml', 'repo_id' => 'repository.kaosbox2', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.kaosbox2/repository.kaosbox2-0.zip?raw=true' ),
		'karrade' => array ( 'name' => 'Karrade\'s XBMC Addons', 'dataUrl' => 'http://github.com/Karrade/xbmc-repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://github.com/Karrade/xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.karrade', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.karrade/repository.karrade-0.zip?raw=true' ),
		'kasiks' => array( 'name' => 'Kasiks Repo', 'dataUrl' => 'https://github.com/Kasik/Kasiks-Repo/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/Kasik/Kasiks-Repo/raw/master/addons.xml', 'repo_id' => 'repository.Kasik', 'zip' => '1', 'downloadUrl' => 'https://github.com/Kasik/Kasiks-Repo/blob/master/zips/repository.Kasik/repository.Kasik-1.1.zip?raw=true' ), 
		'KeesV' => array ( 'name' => 'KeesV Repo', 'dataUrl' => 'https://raw.github.com/KeesV/xbmc-repo/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/KeesV/xbmc-repo/master/addons.xml', 'repo_id' => 'repository.keesv', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.keesv/repository.keesv-0.zip?raw=true' ),
		'kgontv' => array( 'name' => 'KGOnTV XBMC Add-ons', 'dataUrl' => 'http://xbmc-kg-ontv.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-kg-ontv.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.kgontv', 'zip' => '', 'downloadUrl' => 'https://xbmc-kg-ontv.googlecode.com/files/repository.kgontv-1.0.0.zip' ), 
		'kinkin' => array( 'name' => 'Kinkin\'s Repo', 'dataUrl' => 'https://offshoregit.com/kinkin-xbmc-repository/zips/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/kinkin-xbmc-repository/addons.xml', 'repo_id' => 'repository.Kinkin', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/kinkin-xbmc-repository/zips/repository.Kinkin/repository.Kinkin-1.4.zip' ), 
		'kodi-brasil-forum' => array( 'name' => 'Kodi Brasil Forum Repository', 'dataUrl' => 'http://raw.github.com/kodibrasil/kodibrasilforum/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/kodibrasil/kodibrasilforum/master/addons.xml', 'repo_id' => 'repository.kodibrasilforum', 'zip' => '1', 'downloadUrl' => 'https://github.com/kodibrasil/kodibrasilforum/blob/master/repository.kodibrasilforum/repository.kodibrasilforum-1.0.5.zip?raw=true' ), 
		'kodi-czsk' => array( 'name' => 'Kodi CZ and SK Doplnky', 'dataUrl' => 'http://kodi-czsk.github.io/repository/repo/','statsUrl' => '', 'xmlUrl' => 'http://kodi-czsk.github.io/repository/repo/addons.xml', 'repo_id' => 'repository.kodi-czsk', 'zip' => '1', 'downloadUrl' => 'http://kodi-czsk.github.io/repository/repo/repository.kodi-czsk/repository.kodi-czsk-1.0.1.zip' ), 
		'kodi-israel' => array( 'name' => 'www.Kodisrael.co.il Repository', 'dataUrl' => 'https://raw.githubusercontent.com/kodil/kodil/master/repo/','statsUrl' => '', 'xmlUrl' => '>https://raw.githubusercontent.com/kodil/kodil/master/addons.xml', 'repo_id' => 'repository.kodil', 'zip' => '1', 'downloadUrl' => 'http://lvtvv.com/repo/kodil.zip' ),
		'kodi-underground' => array( 'name' => 'Kodi Underground', 'dataUrl' => 'http://kodi.speedbox.me/svn_kodi/trunk/','statsUrl' => '', 'xmlUrl' => 'http://kodi.speedbox.me/svn_kodi/trunk/addons.xml', 'repo_id' => 'repository.kodiunderground', 'zip' => '1', 'downloadUrl' => 'https://github.com/prilly/repository.kodiunderground/releases/download/v1.0.2/repository.kodiunderground-1.0.2.zip' ), 
		'krysty' => array ( 'name' => 'krysty-xbmc addons', 'dataUrl' => 'https://github.com/yokrysty/krysty-xbmc/tree/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/yokrysty/krysty-xbmc/master/addons/addons.xml', 'repo_id' => 'repository.googlecode.krysty-xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.googlecode.krysty-xbmc/repository.googlecode.krysty-xbmc-0.zip?raw=true' ),
		'Kuroshi' => array ( 'name' => 'Kuroshi\'s XBMC Addons', 'dataUrl' => 'http://ramblingahoge.net/kuroshi-xbmc-repo/','statsUrl' => '', 'xmlUrl' => 'http://ramblingahoge.net/kuroshi-xbmc-repo/addons.xml', 'repo_id' => 'repository.kuroshi', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.kuroshi/repository.kuroshi-0.zip?raw=true' ),
		'lambda' => array ( 'name' => 'lambda Add-on repository', 'dataUrl' => 'http://raw.github.com/lambda81/lambda-repo/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/lambda81/lambda-repo/master/addons.xml', 'repo_id' => 'repository.lambda', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.lambda/repository.lambda-0.zip?raw=true' ),
		'Lary_loose' => array ( 'name' => 'Lary_Loose Repository', 'dataUrl' => 'https://github.com/LaryLoose/laryloose.xbmc-addons/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/LaryLoose/laryloose.xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.laryloose.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.laryloose.xbmc-addons/repository.laryloose.xbmc-addons-0.zip?raw=true' ),
		'Leandros' => array ( 'name' => 'Leandros Repository', 'dataUrl' => 'http://xbmcrepo.arvid-g.de/','statsUrl' => '', 'xmlUrl' => 'http://xbmcrepo.arvid-g.de/addons.xml', 'repo_id' => 'repository.leandros.xbmc-plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.leandros.xbmc-plugins/repository.leandros.xbmc-plugins-0.zip?raw=true' ),
		'Leopold' => array ( 'name' => 'Leopold\'s Add-ons', 'dataUrl' => 'https://raw.github.com/LS80/repository.leopold/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/LS80/repository.leopold/master/addons.xml', 'repo_id' => 'xbmc.repo.leopold', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.leopold/xbmc.repo.leopold-0.zip?raw=true' ),
		'LIN' => array( 'name' => 'LIN XBMC Add-ons', 'dataUrl' => 'https://github.com/totalinstall/manual-updates/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://linspb.us/xbmc/addons.xml', 'repo_id' => 'repository.lin', 'zip' => '', 'downloadUrl' => 'http://linspb.us/xbmc/repository.lin.zip' ), 
		'liquid8d' => array ( 'name' => 'liquid8d\'s XBMC Addons', 'dataUrl' => 'https://raw.github.com/liquid8d/xbmc/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/liquid8d/xbmc/master/addons.xml', 'repo_id' => 'repository.liquid8d', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.liquid8d/repository.liquid8d-0.zip?raw=true' ),
		'lordindy' => array( 'name' => 'lordindy add-on repository', 'dataUrl' => 'http://lordindy-xbmc.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://lordindy-xbmc.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.googlecode.lordindy', 'zip' => '1', 'downloadUrl' => 'http://lordindy-xbmc.googlecode.com/svn/addons/repository.googlecode.lordindy/repository.googlecode.lordindy-1.0.0.zip' ), 
		'L0RE' => array ( 'name' => 'Repo Lost and Found', 'dataUrl' => 'https://raw.githubusercontent.com/kodinerds/repo/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/kodinerds/repo/master/addons.xml', 'repo_id' => 'repository.lost-and-found', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.lost-and-found/repository.lost-and-found-0.zip?raw=true' ),
		'lsellens' => array ( 'name' => 'lsellens openelec addon repository', 'dataUrl' => 'http://lsellens.openelec.tv/addons/repo/','statsUrl' => '', 'xmlUrl' => 'http://lsellens.openelec.tv/addons/repo/addons.xml', 'repo_id' => 'repository.lsellens', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.lsellens/repository.lsellens-0.zip?raw=true' ),
		'Lunatixz' => array ( 'name' => 'Lunatixz Repo', 'dataUrl' => 'http://raw.github.com/Lunatixz/XBMC_Addons/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Lunatixz/XBMC_Addons/master/addons.xml', 'repo_id' => 'repository.lunatixz', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.lunatixz/repository.lunatixz-0.zip?raw=true' ),
		'luxeria' => array( 'name' => 'Luxeria Add-ons', 'dataUrl' => 'http://luxeria-repository.googlecode.com/svn/trunk/luxeria/','statsUrl' => '', 'xmlUrl' => 'http://luxeria-repository.googlecode.com/svn/trunk/luxeria//addons.xml', 'repo_id' => 'repository.luxeria', 'zip' => '1', 'downloadUrl' => 'https://luxeria-repository.googlecode.com/files/repository.luxeria.zip' ), 
		'Lynx187' => array ( 'name' => 'xStream Repository', 'dataUrl' => 'http://raw.github.com/Lynx187/xStreamRepo/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Lynx187/xStreamRepo/master/addons.xml', 'repo_id' => 'repository.xstream', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xstream/repository.xstream-0.zip?raw=true' ),
		'm0ngr31' => array( 'name' => 'm0ngr31\'s Add-on Repository', 'dataUrl' => 'http://m0ngr31.us/repo/download/','statsUrl' => '', 'xmlUrl' => 'http://m0ngr31.us/repo/addons.xml', 'repo_id' => 'repository.m0ngr31', 'zip' => '', 'downloadUrl' => 'http://m0ngr31.us/repo/repository.m0ngr31.zip' ), 
		'm3g4mInD' => array ( 'name' => 'm3g4mInD.repository repository', 'dataUrl' => 'http://raw.github.com/m3g4mInD/m3g4mInD.repository/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/m3g4mInD/m3g4mInD.repository/master/addons.xml', 'repo_id' => 'm3g4mInD.repository', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/m3g4mInD.repository/m3g4mInD.repository-0.zip?raw=true' ),
		'm4x1m' => array ( 'name' => 'Max (m4x1m) Headroom XBMC AddOns Repository', 'dataUrl' => 'https://calm-river-6855.herokuapp.com/repository/','statsUrl' => '', 'xmlUrl' => 'https://calm-river-6855.herokuapp.com/repository/addons.xml', 'repo_id' => 'repository.m4x1m', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.m4x1m/repository.m4x1m-0.zip?raw=true' ),
		'mablae' => array ( 'name' => 'NordishByNature Addons', 'dataUrl' => 'http://github.com/mablae/xbmc-repo-nordish-by-nature/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/mablae/xbmc-repo-nordish-by-nature/master/addons.xml', 'repo_id' => 'xbmc.repo.nordish-by-nature', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/xbmc.repo.nordish-by-nature/xbmc.repo.nordish-by-nature-0.zip?raw=true' ),
		'macedoniaondemand' => array( 'name' => 'Macedonia On Demand Add-on Repository', 'dataUrl' => 'http://macedoniaondemand.googlecode.com/git/','statsUrl' => '', 'xmlUrl' => 'http://macedoniaondemand.googlecode.com/git/addons.xml', 'repo_id' => 'repository.macedoniaondemand.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://macedoniaondemand.googlecode.com/files/repository.macedoniaondemand.xbmc-plugins.zip' ), 
		'maffaricos' => array( 'name' => 'Mafarricos Add-on Repository', 'dataUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-xbmc-addons/master/addons.xml', 'repo_id' => 'repository.mafarricos.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/Mafarricos/Mafarricos-xbmc-addons/blob/master/repo/repository.mafarricos.xbmc/repository.mafarricos.xbmc-1.0.5.zip?raw=true' ), 
		'Mafarricos' => array ( 'name' => 'Mafarricos Dev repositorio', 'dataUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-xbmc-dev-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-xbmc-dev-addons/master/addons.xml', 'repo_id' => 'repository.mafarricosDev.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mafarricosDev.xbmc/repository.mafarricosDev.xbmc-0.zip?raw=true' ),
		'maffaricos_modded' => array( 'name' => 'Mafarricos Modded Add-on Repository', 'dataUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-modded-xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Mafarricos/Mafarricos-modded-xbmc-addons/master/addons.xml', 'repo_id' => 'repository.mafarricosModded.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/Mafarricos/Mafarricos-xbmc-addons/blob/master/repo/repository.mafarricosModded.xbmc/repository.mafarricosModded.xbmc-1.0.1.zip?raw=true' ), 
		'MagicTR-Team' => array ( 'name' => 'MagicTR Add-on Repository', 'dataUrl' => 'https://github.com/koditr/magic-tr-team/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/koditr/magic-tr-team/raw/master/addons.xml', 'repo_id' => 'magicTR.repo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/magicTR.repo/magicTR.repo-0.zip?raw=true' ),
		'malaysia' => array ( 'name' => 'Malaysia XBMC Addon Repository', 'dataUrl' => 'http://malaysia-kodiaddon-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://malaysia-kodiaddon-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.malayxbmc.addons', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.malayxbmc.addons/repository.malayxbmc.addons-0.zip?raw=true' ),
		'Maniac' => array ( 'name' => 'Maniac\'s Add-on Repository', 'dataUrl' => 'http://github.com/manijak/repository.maniac/raw/master/helix/','statsUrl' => '', 'xmlUrl' => 'http://github.com/manijak/repository.maniac/raw/master/helix/addons.xml', 'repo_id' => 'repository.maniac', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.maniac/repository.maniac-0.zip?raw=true' ),
		'mancuniancol,iCanuck' => array ( 'name' => 'Pulsar Unofficial Repo', 'dataUrl' => 'http://offshoregit.com/pulsarunofficial/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/pulsarunofficial/raw/master/addons.xml', 'repo_id' => 'repository.pulsarunofficial', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.pulsarunofficial/repository.pulsarunofficial-0.zip?raw=true' ),
		'mancuniancol,iCanuck' => array ( 'name' => 'Pulsar Unofficial Repo Mirror', 'dataUrl' => 'http://offshoregit.com/iCanuck/Unofficial-Pulsar-Repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/iCanuck/Unofficial-Pulsar-Repo/raw/master/addons.xml', 'repo_id' => 'repository.pulsarunofficialmirror', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.pulsarunofficialmirror/repository.pulsarunofficialmirror-0.zip?raw=true' ),
		'maruchan' => array( 'name' => 'Maruchan\'s Add-ons', 'dataUrl' => 'http://xbmc-addon-repository.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-addon-repository.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.unofficial.addons', 'zip' => '', 'downloadUrl' => 'https://xbmc-addon-repository.googlecode.com/files/repository.unofficial.addons.zip' ), 
		'massivept' => array( 'name' => 'MassivePt Add-on Repository', 'dataUrl' => 'http://massive-pt.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://massive-pt.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.googlecode.massive-pt', 'zip' => '1', 'downloadUrl' => 'https://massive-pt.googlecode.com/svn/trunk/repository.googlecode.massive-pt/repository.googlecode.massive-pt-1.1.3.zip' ), 
		'maxmustermann' => array( 'name' => 'MaxMustermann\'s Add-ons', 'dataUrl' => 'http://xbmc-development-with-passion.googlecode.com/svn/branches/repo/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-development-with-passion.googlecode.com/svn/branches/repo/addons.xml', 'repo_id' => 'repository.MaxMustermann.xbmc', 'zip' => '1', 'downloadUrl' => 'http://xbmc-development-with-passion.googlecode.com/svn/branches/repo/repository.MaxMustermann.xbmc/repository.MaxMustermann.xbmc-1.0.1.zip' ),
		'MazurokNN' => array ( 'name' => 'MNN Xbmc Add-ons', 'dataUrl' => 'https://github.com/snakefishh/mnn-xbmc-repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/snakefishh/mnn-xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.mnn', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mnn/repository.mnn-0.zip?raw=true' ),
		'membrane' => array( 'name' => 'membrane\'s repository', 'dataUrl' => 'http://membrane-xbmc-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://membrane-xbmc-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.membrane.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://membrane-xbmc-repo.googlecode.com/files/repository.membrane.xbmc-plugins.zip' ), 
		'metalkettle' => array( 'name' => 'metalkettle\'s Repo', 'dataUrl' => 'http://offshoregit.com/metalkettle/zips/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/metalkettle/addons.xml', 'repo_id' => 'repository.metalkettle', 'zip' => '1', 'downloadUrl' => 'https://github.com/metalkettle/MetalKettles-Addon-Repository/blob/master/zips/repository.metalkettle/repository.metalkettle-1.6.2.zip?raw=true' ), 
// Gone		'metalkettlem2k' => array( 'name' => 'MoviesHD Addon Repository', 'dataUrl' => 'http://raw.github.com/metalkettle/MoviesHD/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/metalkettle/MoviesHD/master/addons.xml', 'repo_id' => 'repository.movieshd', 'zip' => '1', 'downloadUrl' => 'https://github.com/metalkettle/MoviesHD/blob/master/zips/repository.movieshd/repository.movieshd-1.0.1.zip?raw=true' ), 
/* merged into xunitytalk repo */		'mikey1234' => array( 'name' => 'Mikey1234 Add-ons', 'dataUrl' => 'http://mikey1234-repo.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => 'repository.mikey1234', 'zip' => '1', 'downloadUrl' => 'http://xty.me/xunitytalk/addons/repository.xunitytalk/repository.xunitytalk-1.0.3.zip' ), 
		'mikaelec' => array ( 'name' => 'mikaelec\'s XBMC Addons', 'dataUrl' => 'https://raw.github.com/mikaelec/mikaelec-xbmc-repo/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/mikaelec/mikaelec-xbmc-repo/master/addons.xml', 'repo_id' => 'repository.mikaelec', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mikaelec/repository.mikaelec-0.zip?raw=true' ),
/* site still up but addon.xml gone */		'mindmade' => array ( 'name' => 'mindmade XBMC Addons', 'dataUrl' => 'http://www.mindmade.org/~andi/xbmc/addons/','statsUrl' => '', 'xmlUrl' => 'http://www.mindmade.org/~andi/xbmc/addons/addons.xml', 'repo_id' => 'repository.mindmade', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mindmade/repository.mindmade-0.zip?raw=true' ),
		'MisterX' => array ( 'name' => 'MisterX Adult Repository', 'dataUrl' => 'https://raw.github.com/MisterXx/MisterX/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/MisterXx/MisterX/master/addons.xml', 'repo_id' => 'repository.MisterX', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.MisterX/repository.MisterX-0.zip?raw=true' ),
		'mko' => array( 'name' => 'mKo\'s Add-on Repository', 'dataUrl' => 'http://xbmc-repo-mko.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-repo-mko.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.mko', 'zip' => '1', 'downloadUrl' => 'https://xbmc-repo-mko.googlecode.com/files/repository.mko.zip' ), 
// Gone		'morstar' => array ( 'name' => 'repository.mortstar.addons', 'dataUrl' => 'https://github.com/mortstar/repository-mortstar-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/mortstar/repository-mortstar-addons/raw/master/addons.xml', 'repo_id' => 'repository.mortstar.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mortstar.addons/repository.mortstar.addons-0.zip?raw=true' ),
		'mossy' => array( 'name' => 'Mossy\'s Frodo Repo', 'dataUrl' => 'http://mossy-xbmc-repo.googlecode.com/git/release/','statsUrl' => '', 'xmlUrl' => 'http://mossy-xbmc-repo.googlecode.com/git/release/addons.xml', 'repo_id' => 'repository.mossy', 'zip' => '1', 'downloadUrl' => 'https://mossy-xbmc-repo.googlecode.com/files/repository.mossy.frodo.zip' ), 
		'MQ' => array( 'name' => 'Aeon MQ 3/4 Skin Repo', 'dataUrl' => 'http://mod-skin.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://mod-skin.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.mq', 'zip' => '1', 'downloadUrl' => 'https://mod-skin.googlecode.com/files/repository.mq.zip' ), 
		'mrknowpl' => array ( 'name' => 'Kodi filmkodi.com repository', 'dataUrl' => 'http://filmkodi.com/repository/','statsUrl' => '', 'xmlUrl' => 'http://filmkodi.com/repository/addons.xml', 'repo_id' => 'repository.filmkodi.com', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.filmkodi.com/repository.filmkodi.com-0.zip?raw=true' ),
		'mrstealth' => array( 'name' => 'MrStealth XBMC Add-ons Repository', 'dataUrl' => 'https://raw.github.com/mrstealth/xbmc-plugins/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/mrstealth/xbmc-plugins/master/addons.xml', 'repo_id' => 'repository.mrstealth', 'zip' => '1', 'downloadUrl' => 'https://github.com/mrstealth/xbmc-plugins/raw/master/repo/repository.mrstealth/repository.mrstealth-1.0.4.zip' ), 
		'MrStealth-gotham' => array ( 'name' => 'Mrstealth XBMC Gotham', 'dataUrl' => 'https://raw.github.com/mrstealth/xbmc-gotham/master/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/mrstealth/xbmc-gotham/master/addons.xml', 'repo_id' => 'repository.mrstealth.gotham', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mrstealth.gotham/repository.mrstealth.gotham-0.zip?raw=true' ),
		'muckyduck' => array( 'name' => 'Mucky Ducks Repo', 'dataUrl' => 'https://raw.githubusercontent.com/mucky-duck/mdrepo/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/mucky-duck/mdrepo/master/addons.xml', 'repo_id' => 'repository.mdrepo', 'zip' => '1', 'downloadUrl' => 'http://muckys.kodimediaportal.ml/repository.mdrepo-1.0.1.zip' ), 
		'mudisle' => array( 'name' => 'Mudisle Repo', 'dataUrl' => 'http://xbmc-skin-convergence.googlecode.com/svn/branches/repo/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-skin-convergence.googlecode.com/svn/branches/repo/addons.xml', 'repo_id' => 'xbmc.repo.mudisle', 'zip' => '', 'downloadUrl' => 'https://xbmc-skin-convergence.googlecode.com/files/xbmc.repo.mudisle-v1.0.1.zip' ), 
/* addon.xml seems messed up */		'mx' => array( 'name' => 'MX Add-on Repository', 'dataUrl' => 'http://thaisatellite.tv/repo/','statsUrl' => '', 'xmlUrl' => 'http://thaisatellite.tv/repo/addons.xml', 'repo_id' => 'repository.mx', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mx/repository.mx-0.zip?raw=true' ),
		'myshows-me' => array( 'name' => 'MyShows.me Kodi Repo', 'dataUrl' => 'http://api.bitbucket.org/1.0/repositories/DiMartino/myshows.me-kodi-repo/raw/default/repo/','statsUrl' => '', 'xmlUrl' => 'http://api.bitbucket.org/1.0/repositories/DiMartino/myshows.me-kodi-repo/raw/default/addons.xml', 'repo_id' => 'repository.myshows.me', 'zip' => '', 'downloadUrl' => 'https://bitbucket.org/DiMartino/myshows.me-kodi-repo/downloads/repository.myshows.me.zip' ), 
		'nibor' => array( 'name' => 'Nibor\'s Add-ons', 'dataUrl' => 'http://nibor-xbmc-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://nibor-xbmc-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.nibor', 'zip' => '', 'downloadUrl' => 'http://nibor-xbmc-repo.googlecode.com/svn/trunk/repository.nibor.zip' ), 
		'natko1412' => array( 'name' => 'Natko\'s Addon Repository', 'dataUrl' => 'https://offshoregit.com/natko1412/zips/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/natko1412/addons.xml', 'repo_id' => 'repository.natko1412', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/natko1412/zips/repo.natko1412/repo.natko1412-2.0.0.zip' ),
// Gone		'ninbora' => array( 'name' => 'Ninbora Addons', 'dataUrl' => 'http://www.ninbora.com/addons/','statsUrl' => '', 'xmlUrl' => 'http://www.ninbora.com/addons/addons.xml', 'repo_id' => 'repository.nonbora', 'zip' => '1', 'downloadUrl' => 'http://www.ninbora.com/addons/' ),
		'NitroCSIA' => array ( 'name' => 'NitroCSIA\'s XBMC Addons', 'dataUrl' => 'http://raw.github.com/NitroCSIA/nitrocsia-xbmc-addons/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/NitroCSIA/nitrocsia-xbmc-addons/master/addons.xml', 'repo_id' => 'repository.nitrocsia', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.nitrocsia/repository.nitrocsia-0.zip?raw=true' ),
		'nixa' => array( 'name' => 'Nixa\'s Add-ons', 'dataUrl' => 'http://sparetime.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://sparetime.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.sparetime', 'zip' => '', 'downloadUrl' => 'https://sparetime.googlecode.com/files/repository.googlecode.sparetime.zip' ),
		'NJM' => array( 'name' => 'NJM Soccer Repo', 'dataUrl' => 'http://repo.badgersftv.com/repo/','statsUrl' => '', 'xmlUrl' => '>http://repo.badgersftv.com/repo/addons.xml', 'repo_id' => 'repository.NJM Soccer', 'zip' => '1', 'downloadUrl' => 'http://njmweb.we.bs/NJMSoccer/repository.NJMSoccer-0.1.0.zip' ),
// Gone		'NLSPORTS' => array ( 'name' => 'NL Sports Repository', 'dataUrl' => 'http://git.tvaddons.nl:8888/root/NL-Addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://git.tvaddons.nl:8888/root/NL-Addons/raw/master/addons.xml', 'repo_id' => 'repository.nlsports', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.nlsports/repository.nlsports-0.zip?raw=true' ),
		'NoFussComputing' => array( 'name' => 'No Fuss Computings Addons', 'dataUrl' => 'https://raw.github.com/NoFussComputing/nofussrepository/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/NoFussComputing/nofussrepository/master/addons.xml', 'repo_id' => 'repository.nofusscomputing', 'zip' => '1', 'downloadUrl' => 'https://github.com/NoFussComputing/nofussrepository/blob/master/addons/repository.nofusscomputing/repository.nofusscomputing-0.1.zip?raw=true' ), 
		'noobsandnerds' => array ( 'name' => 'noobsandnerds Repository', 'dataUrl' => 'https://raw.githubusercontent.com/noobsandnerds/noobsandnerds/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/noobsandnerds/noobsandnerds/master/zips/addons.xml', 'repo_id' => 'repository.noobsandnerds', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.noobsandnerds/repository.noobsandnerds-0.zip?raw=true' ),
// Gone		'NuisMons' => array( 'name' => 'NuisMons XBMC Add-ons', 'dataUrl' => 'https://raw.github.com/NuisMons/nuXBMCRepo/master/addons/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/NuisMons/nuXBMCRepo/master/addons/addons.xml', 'repo_id' => 'repository.nuismons', 'zip' => '1', 'downloadUrl' => 'https://github.com/NuisMons/nuXBMCRepo/raw/master/addons/repository.nuismons/repository.nuismons-1.0.1.zip' ), 
		'nuka1195' => array( 'name' => 'Nuka1195\'s Add-ons', 'dataUrl' => 'http://xbmc-addons.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-addons.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-addons', 'zip' => '', 'downloadUrl' => '' ), 
		'NVTTeam' => array ( 'name' => 'NVTTeam Repository', 'dataUrl' => 'http://raw.github.com/NVTTeam/NVTTeam-Repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/NVTTeam/NVTTeam-Repo/master/addons.xml', 'repo_id' => 'repository.nvtteam', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.nvtteam/repository.nvtteam-0.zip?raw=true' ),
		'o9r1sh' => array( 'name' => 'o9r1sh\'s Repo', 'dataUrl' => 'http://github.com/o9r1sh/o9r1sh/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://github.com/o9r1sh/o9r1sh/raw/master/addons.xml', 'repo_id' => 'repository.o9r1sh', 'zip' => '1', 'downloadUrl' => 'https://github.com/o9r1sh/o9r1sh/blob/master/zips/repository.o9r1sh/repository.o9r1sh-1.3.zip?raw=true' ), 
		'OMaluco' => array( 'name' => 'Filmes Series Tuga Add-on Repository', 'dataUrl' => 'http://o-repositorio-maluco.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://o-repositorio-maluco.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'o.repository.maluco', 'zip' => '0', 'downloadUrl' => 'http://o-repositorio-maluco.googlecode.com/svn/trunk/downloads/o.repository.maluco.zip' ), 
// Gone		'p2pStreams' => array( 'name' => 'P2P Streams Repo', 'dataUrl' => 'http://p2p-strm.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://p2p-strm.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.p2p-streams.xbmc', 'zip' => '1', 'downloadUrl' => 'https://p2p-strm.googlecode.com/svn/addons/repository.p2p-streams.xbmc/repository.p2p-streams.xbmc-1.0.4.zip' ), 
/* old, now newer version on hub repo */		'parental-controls' => array( 'name' => 'XBMC Parental Controls Repository', 'dataUrl' => 'https://github.com/killdash9/xbmc-parental-controls/raw/master/repo/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => 'script.video.parentalcontrols', 'zip' => '1', 'downloadUrl' => 'https://github.com/killdash9/xbmc-parental-controls/blob/master/repo/script.video.parentalcontrols/script.video.parentalcontrols-1.5.3.zip?raw=true' ), 
		'passion-frodo' => array( 'name' => 'Passion XBMC Repo Frodo', 'dataUrl' => 'http://passion-xbmc.org/addons/Download.php/','statsUrl' => '', 'xmlUrl' => 'http://passion-xbmc.org/addons/addons.php/12.0', 'repo_id' => 'repository.passion.xbmc.org.frodo', 'zip' => '', 'downloadUrl' => 'http://passion-xbmc.org/addons/Download.php/repository.passion.xbmc.org.frodo/repository.passion.xbmc.org.frodo-3.0.1.zip' ), 
		'passion-gotham' => array( 'name' => 'Passion XBMC Repo Gotham', 'dataUrl' => 'http://passion-xbmc.org/addons/Download.php/','statsUrl' => '', 'xmlUrl' => 'http://passion-xbmc.org/addons/addons.php/13.0', 'repo_id' => 'repository.passion.xbmc.org.gotham', 'zip' => '', 'downloadUrl' => 'http://passion-xbmc.org/addons/Download.php/repository.passion.xbmc.org.gotham/repository.passion.xbmc.org.gotham-4.0.0.zip' ), 
		'passion-helix' => array( 'name' => 'Passion XBMC Repo Helix', 'dataUrl' => 'http://passion-xbmc.org/addons/Download.php/','statsUrl' => '', 'xmlUrl' => 'http://passion-xbmc.org/addons/addons.php/14.0', 'repo_id' => 'repository.passion.xbmc.org.gotham', 'zip' => '', 'downloadUrl' => '' ), 
		'pcd' => array( 'name' => 'PCD\'s Repository', 'dataUrl' => 'https://offshoregit.com/pcd/pcd-repo/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/pcd/pcd-repo/addons.xml', 'repo_id' => 'repository.pcd', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/pcd/pcd-repo/repository.pcd/repository.pcd-1.0.zip' ), 
		'PENguine' => array ( 'name' => 'PENguine Addon Repository', 'dataUrl' => 'https://raw.github.com/PEN-guine/Kodi-Stuff/master/deployments/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/PEN-guine/Kodi-Stuff/master/deployments/addons.xml', 'repo_id' => 'repository.penguine', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.penguine/repository.penguine-0.zip?raw=true' ),
		'Petr Kutalek' => array ( 'name' => 'Aktualne TV Add-on Repository', 'dataUrl' => 'https://github.com/petrkutalek/plugin.video.aktualnetv/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/petrkutalek/plugin.video.aktualnetv/raw/master/addons.xml', 'repo_id' => 'repository.aktualnetv', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.aktualnetv/repository.aktualnetv-0.zip?raw=true' ),
		'phoenix' => array( 'name' => 'Phoenix Addon Repository', 'dataUrl' => 'https://xbmc-phoenix.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'https://xbmc-phoenix.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-phoenix', 'zip' => '1', 'downloadUrl' => 'https://xbmc-phoenix.googlecode.com/files/repository.googlecode.xbmc-phoenix.zip' ), 
		'phuoclv' => array ( 'name' => 'Cantobu Media Repository', 'dataUrl' => 'https://raw.githubusercontent.com/phuoclv/repository.cantobumedia/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/phuoclv/repository.cantobumedia/master/addons.xml', 'repo_id' => 'repository.cantobumedia', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.cantobumedia/repository.cantobumedia-0.zip?raw=true' ),
		'pietervanh' => array( 'name' => 'pietervanh\'s repo', 'dataUrl' => 'https://github.com/pietervanh/xbmc-repository-pietervanh/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/pietervanh/xbmc-repository-pietervanh/raw/master/addons.xml', 'repo_id' => 'repository.pietervanh.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.pietervanh.addons/repository.pietervanh.addons-0.zip?raw=true' ),
		'pipcan' => array( 'name' => 'pipcan\'s repo', 'dataUrl' => 'http://raw.github.com/pipcan3/Pipcan-Repo/master/_repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/pipcan3/Pipcan-Repo/master/_repo/addons.xml', 'repo_id' => 'repository.pipcan', 'zip' => '1', 'downloadUrl' => 'https://github.com/pipcan3/Pipcan-Repo/blob/master/_repo/repository.pipcan/repository.pipcan-1.0.2.zip.20151012162337?raw=true' ), 
		'podgod' => array( 'name' => 'podgod repo', 'dataUrl' => 'http://offshoregit.com/podgod/repo/zips/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/podgod/repo/addons.xml', 'repo_id' => 'repository.podgod', 'zip' => '1', 'downloadUrl' => 'http://podgod.mtlfreetv.com/Podgod/install/repository.podgod-1.7.zip' ), 
		'polskie_wtyczki' => array( 'name' => 'Polskie Wtyczki Add-ons', 'dataUrl' => 'http://raw.github.com/xbmc-addons-polish/polskie_wtyczki/master/download/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/xbmc-addons-polish/polskie_wtyczki/master/addons.xml', 'repo_id' => 'repository.unofficial.polish', 'zip' => '1', 'downloadUrl' => 'https://github.com/xbmc-addons-polish/polskie_wtyczki/blob/master/download/repository.unofficial.polish/repository.unofficial.polish-2.0.0.zip?raw=true' ), 
		'popcornmix' => array( 'name' => 'Popcornmix Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/popcornmix/repository.popcornmix.storage/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/popcornmix/repository.popcornmix.storage/raw/master/addons.xml', 'repo_id' => 'repository.popcornmix', 'zip' => '1', 'downloadUrl' => 'https://github.com/popcornmix/repository.popcornmix.storage/raw/master/repository.popcornmix.zip' ), 
		'popcorntime' => array( 'name' => 'KODI Popcorn Time Repository', 'dataUrl' => 'http://raw.githubusercontent.com/Diblo/KODI-Popcorn-Time/Repository/','statsUrl' => '', 'xmlUrl' => 'http://raw.githubusercontent.com/Diblo/KODI-Popcorn-Time/Repository/addons.xml', 'repo_id' => 'repository.kodipopcorntime', 'zip' => '1', 'downloadUrl' => 'https://raw.githubusercontent.com/Diblo/KODI-Popcorn-Time/Repository/repository.kodipopcorntime/repository.kodipopcorntime-1.0.2.zip' ), 
		'popeye' => array( 'name' => 'Popeye\'s Repo', 'dataUrl' => 'https://raw.github.com/TsUPeR/xbmc-repo/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/TsUPeR/xbmc-repo/master/addons.xml', 'repo_id' => 'repository.popeye', 'zip' => '1', 'downloadUrl' => 'https://github.com/TsUPeR/xbmc-repo/blob/master/repo/repository.popeye/repository.popeye-1.0.1.zip?raw=true' ), 
		'prafit' => array( 'name' => 'Prafit Repository', 'dataUrl' => 'http://github.com/prafit/prafit/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://github.com/prafit/prafit/raw/master/addons.xml', 'repo_id' => 'repository.prafit', 'zip' => '1', 'downloadUrl' => 'https://github.com/prafit/prafit/blob/master/zips/repository.prafit/repository.prafit-1.0.zip?raw=true' ), 
		'proteusplum' => array ( 'name' => 'mFlow XBMC Addon', 'dataUrl' => 'https://github.com/proteusplum/mflow-xbmc-plugin-repo/raw/master/downloads/','statsUrl' => '', 'xmlUrl' => 'https://github.com/proteusplum/mflow-xbmc-plugin-repo/raw/master/addons.xml', 'repo_id' => 'repository.mFlow', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mFlow/repository.mFlow-0.zip?raw=true' ),
		'ptom' => array ( 'name' => 'PTOM Repo', 'dataUrl' => 'http://ptom.co.uk/repo/','statsUrl' => '', 'xmlUrl' => 'http://ptom.co.uk/repo/addons.xml', 'repo_id' => 'repository.ptom', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.ptom/repository.ptom-0.zip?raw=true' ),
		'pulsar_providers_unofficial' => array ( 'name' => 'Pulsar Providers Unofficial Repo', 'dataUrl' => 'http://offshoregit.com/pulsarunofficial/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://offshoregit.com/pulsarunofficial/raw/master/addons.xml', 'repo_id' => 'repository.providerspulsarunofficial', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.providerspulsarunofficial/repository.providerspulsarunofficial-0.zip?raw=true' ),
		'pulsar_unofficial' => array( 'name' => 'Pulsar Unofficial Repo', 'dataUrl' => 'https://github.com/icanuck/Unofficial-Pulsar-Repo-Mirror/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/icanuck/Unofficial-Pulsar-Repo-Mirror/raw/master/addons.xml', 'repo_id' => 'repository.pulsarunofficial', 'zip' => '1', 'downloadUrl' => 'https://icanuckxbmcrepo.svn.cloudforge.com/pulsarunofficialrepo/trunk/repository.pulsarunofficial/repository.pulsarunofficial-1.0.1.zip' ), 
		'pulsar_unofficial_mirror' => array( 'name' => 'Pulsar Unofficial Repo', 'dataUrl' => 'https://icanuckxbmcrepo.svn.cloudforge.com/pulsarunofficialrepo/trunk/','statsUrl' => '', 'xmlUrl' => 'https://icanuckxbmcrepo.svn.cloudforge.com/pulsarunofficialrepo/trunk/addons.xml', 'repo_id' => 'repository.pulsarunofficialmirror', 'zip' => '1', 'downloadUrl' => 'https://icanuckxbmcrepo.svn.cloudforge.com/pulsarunofficialrepo/trunk/repository.pulsarunofficialmirror/repository.pulsarunofficialmirror-1.0.0.zip' ), 
		'QF' => array( 'name' => 'QF Add-ons', 'dataUrl' => 'https://github.com/vikjon0/qf-xbmc-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/vikjon0/qf-xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.qf.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/vikjon0/qf-xbmc-addons/blob/master/repo/repository.qf.addons/repository.qf.addons-1.0.1.zip?raw=true' ), 
		'quebec' => array( 'name' => 'Quebec XBMC Repository', 'dataUrl' => 'http://quebec-xbmc-plugin.googlecode.com/svn/zip/','statsUrl' => '', 'xmlUrl' => 'https://quebec-xbmc-plugin.googlecode.com/svn/zip/addons.xml', 'repo_id' => 'repository.infologiqueTV', 'zip' => '1', 'downloadUrl' => '' ), 
		'queeup' => array( 'name' => 'Queeup Add-ons', 'dataUrl' => 'http://raw.github.com/queeup/repository.queeup/frodo/download/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/queeup/repository.queeup/frodo/addons.xml', 'repo_id' => 'repository.queeup', 'zip' => '1', 'downloadUrl' => 'https://github.com/queeup/repository.queeup/blob/gotham/repository.queeup.zip?raw=true' ), 
		'queeup-gotham' => array ( 'name' => 'queeup Add-ons', 'dataUrl' => 'http://raw.github.com/queeup/repository.queeup/gotham/download/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/queeup/repository.queeup/gotham/addons.xml', 'repo_id' => 'repository.queeup', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.queeup/repository.queeup-0.zip?raw=true' ),
// Password Protected		'r3b00t' => array( 'name' => 'Rr3b00t XBMC Plugins', 'dataUrl' => 'https://the-gizmo.svn.beanstalkapp.com/gizmo/addons/','statsUrl' => '', 'xmlUrl' => 'https://the-gizmo.svn.beanstalkapp.com/gizmo/addons/addons.xml', 'repo_id' => 'repository.r3b00t', 'zip' => '1', 'downloadUrl' => 'https://the-gizmo.svn.beanstalkapp.com/gizmo/addons/repository.r3b00t/repository.r3b00t-0.0.1.zip' ), 
		'RAM FM Eighties Hit Radio' => array ( 'name' => 'RAM FM Eighties Hit Radio', 'dataUrl' => 'https://spoyser-repo.googlecode.com/git/zips/','statsUrl' => '', 'xmlUrl' => 'https://spoyser-repo.googlecode.com/git/RAM.FM/addons.xml', 'repo_id' => 'repository.ramfm', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.ramfm/repository.ramfm-0.zip?raw=true' ),
		'rasjani' => array( 'name' => 'Rasjani\'s Repo', 'dataUrl' => 'http://pcuf.fi/~rasjani/xbmc-rasjanisrepo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/rasjani/xbmc-rasjanisrepo/master/addons.xml', 'repo_id' => 'repository.rasjanisrepo.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/rasjani/xbmc-rasjanisrepo/blob/master/repository.rasjanisrepo.xbmc/repository.rasjanisrepo.xbmc-1.0.0.zip?raw=true' ), 
// This is the newer one but it doesn't work		'rasjani' => array ( 'name' => 'Rasjani\'s Add-ons', 'dataUrl' => 'http://pcuf.fi/~rasjani/xbmc-rasjanisrepo/','statsUrl' => '', 'xmlUrl' => 'http://pcuf.fi/~rasjani/xbmc-rasjanisrepo/addons.xml', 'repo_id' => 'repository.rasjanisrepo.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.rasjanisrepo.xbmc/repository.rasjanisrepo.xbmc-0.zip?raw=true' ),
		'Rato' => array ( 'name' => 'Rato-TV repository', 'dataUrl' => ' http://kodi.ratotv.net/repo/','statsUrl' => '', 'xmlUrl' => 'http://kodi.ratotv.net/addons.xml', 'repo_id' => 'repository.rato.tv', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.rato.tv/repository.rato.tv-0.zip?raw=true' ),
		'rawmaintenance' => array( 'name' => 'Raw Media\'s Kodi Add-ons', 'dataUrl' => 'http://raw.github.com/rawmedia/raw_maintenance/master/rawmaintenance_repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/rawmedia/raw_maintenance/master/rawmaintenance_repo/addons.xml', 'repo_id' => 'repository.rawmaintenance', 'zip' => '1', 'downloadUrl' => 'https://github.com/rawmedia/raw_maintenance/blob/master/rawmaintenance_repo/repository.rawmaintenance/repositoy.rawmaintenance.zip?raw=true' ), 
		'rayw1986' => array( 'name' => 'RayW1986 Repo', 'dataUrl' => 'http://raw.github.com/RayW1986/repository.rayw1986/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/RayW1986/repository.rayw1986/master/addons.xml', 'repo_id' => 'repository.rayw1986', 'zip' => '1', 'downloadUrl' => 'http://raw.github.com/RayW1986/repository.rayw1986/master/zips/repository.rayw1986/repository.rayw1986-1.0.zip' ), 
		'regss' => array( 'name' => 'Regss Add-ons', 'dataUrl' => 'https://raw.github.com/Regss/xbmc-regss-repository/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/Regss/xbmc-regss-repository/master/addons.xml', 'repo_id' => 'repository.regss', 'zip' => '1', 'downloadUrl' => 'https://github.com/Regss/xbmc-regss-repository/blob/master/repo/repository.regss/repository.regss-1.2.1.zip?raw=true' ), 
		'rivy' => array ( 'name' => 'RIVY XBMC Repository', 'dataUrl' => 'https://raw.github.com/rivy/xbmc-repository/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/rivy/xbmc-repository/master/addons.xml', 'repo_id' => 'repository.rivy.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.rivy.xbmc/repository.rivy.xbmc-0.zip?raw=true' ),
// Password protected		'robwebset' => array( 'name' => 'robwebset\'s XBMC Addons', 'dataUrl' => 'http://robwebset.googlecode.com/svn/releases/','statsUrl' => '', 'xmlUrl' => 'http://robwebset.googlecode.com/svn/releases/addons.xml', 'repo_id' => 'repository.robwebset', 'zip' => '1', 'downloadUrl' => 'http://robwebset.googlecode.com/svn/releases/repository.robwebset/repository.robwebset-1.0.0.zip' ), 
		'Rodrigo' => array ( 'name' => 'Rodrigo\'s Repository', 'dataUrl' => 'https://raw.github.com/Rodrigoke/XBMC.repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/rodrigoke/XBMC.repo/master/addons.xml', 'repo_id' => 'repository.Rodrigo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.Rodrigo/repository.Rodrigo-0.zip?raw=true' ),
		'RTPplay' => array( 'name' => 'RTP Play Portugese Repo', 'dataUrl' => 'https://github.com/totalinstall/manual-updates/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://plugin-video-rtpplay-xbmc.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.RTPplay.xbmc', 'zip' => '', 'downloadUrl' => 'https://plugin-video-rtpplay-xbmc.googlecode.com/files/repository.RTPplay.xbmc.zip' ), 
		'ruuk' => array ( 'name' => 'ruuk\'s Repo', 'dataUrl' => 'https://raw.githubusercontent.com/ruuk/repository/master/beta/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/ruuk/repository/master/beta/addons.xml', 'repo_id' => 'ruuk.addon.repository', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/ruuk.addon.repository/ruuk.addon.repository-0.zip?raw=true' ),
		'ruxton' => array ( 'name' => 'Ruxton\'s XBMC Addons', 'dataUrl' => 'https://github.com/Ruxton/xbmc-addon-repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/Ruxton/xbmc-addon-repo/master/addons.xml', 'repo_id' => 'repository.ruxton', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.ruxton/repository.ruxton-0.zip?raw=true' ),
		'salem' => array( 'name' => 'Salem\'s Add-on Repository', 'dataUrl' => 'http://skin-refocusbig.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://skin-refocusbig.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.salem', 'zip' => '1', 'downloadUrl' => 'http://skin-refocusbig.googlecode.com/svn/trunk/repository.salem.zip' ), 
		'sandalov' => array( 'name' => 'Dmitry Sandalov\'s XBMC Repo', 'dataUrl' => 'https://raw.githubusercontent.com/DmitrySandalov/xbmc-repo/master/repo/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/DmitrySandalov/xbmc-repo/master/addons/addons.xml', 'repo_id' => 'repository.sandalov', 'zip' => '1', 'downloadUrl' => 'https://github.com/DmitrySandalov/xbmc-repo/blob/master/repo/zip/repository.sandalov/repository.sandalov.zip?raw=true' ), 
		'sapo' => array ( 'name' => 'XBMC on SAPO', 'dataUrl' => 'https://raw.github.com/sapo/xbmc-repo/master/release/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/sapo/xbmc-repo/master/addons.xml', 'repo_id' => 'repository.sapo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.sapo/repository.sapo-0.zip?raw=true' ),
		'SastaTv' => array( 'name' => 'Sastatv Repository', 'dataUrl' => 'https://github.com/totalinstall/manual-updates/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://sastatv.com/repo/addons.xml', 'repo_id' => '', 'zip' => '', 'downloadUrl' => '' ), 
		'ScudLee' => array( 'name' => 'SudLee\'s Add-on Repository', 'dataUrl' => 'https://github.com/ScudLee/scudlee-xbmc-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/ScudLee/scudlee-xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.scudlee', 'zip' => '1', 'downloadUrl' => 'https://github.com/ScudLee/scudlee-xbmc-addons/blob/master/repo/repository.scudlee/repository.scudlee-1.0.0.zip?raw=true' ), 
		'SD-XBMC' => array( 'name' => 'SD Polish XBMC Repository', 'dataUrl' => 'http://sd-xbmc.org/repository/','statsUrl' => '', 'xmlUrl' => 'http://sd-xbmc.org/repository/addons.xml', 'repo_id' => 'repository.sd-xbmc.org', 'zip' => '1', 'downloadUrl' => '' ), 
		'seppius' => array ( 'name' => 'Seppius XBMC Add-ons', 'dataUrl' => 'https://github.com/seppius-xbmc-repo/ru/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/seppius-xbmc-repo/ru/raw/master/addons.xml', 'repo_id' => 'repository.seppius', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.seppius/repository.seppius-0.zip?raw=true' ),
		'ShadowCrew' => array( 'name' => 'Shadow Crew\'s Add-ons', 'dataUrl' => 'http://shadowsrepo.info/repo/zips/','statsUrl' => '', 'xmlUrl' => 'http://shadowsrepo.info/repo/addons.xml', 'repo_id' => 'repository.shadowcrew', 'zip' => '1', 'downloadUrl' => 'http://shadowsrepo.info/shadows/rhrepository.zip' ),
		'shaiu' => array( 'name' => 'Shaiu\'s Add-ons', 'dataUrl' => 'https://raw.github.com/shaiu/shaiu-xbmc-repo/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/shaiu/shaiu-xbmc-repo/master/addons.xml', 'repo_id' => 'repository.liquid8d', 'zip' => '1', 'downloadUrl' => 'https://github.com/shaiu/xbmc/blob/master/repo/repository.liquid8d/repository.liquid8d-1.0.0.zip?raw=true' ), 
		'shani' => array( 'name' => 'shani Add-ons', 'dataUrl' => 'https://raw.github.com/Shani-08/ShaniXBMCWork/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/Shani-08/ShaniXBMCWork/master/addons.xml', 'repo_id' => 'repository.shani', 'zip' => '', 'downloadUrl' => 'https://github.com/Shani-08/ShaniXBMCWork/blob/master/zips/repository.shani/repository.shani-2.6.zip?raw=true' ), 
		'Shev83' => array ( 'name' => 'RedCouchTV repositorio', 'dataUrl' => 'http://raw.github.com/Shev83/repository.redcouch.xbmc/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Shev83/repository.redcouch.xbmc/master/addons.xml', 'repo_id' => 'repository.redcouch.xbmc', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.redcouch.xbmc/repository.redcouch.xbmc-0.zip?raw=true' ),
		'sickbeard' => array( 'name' => 'Sickbeard integration into XBMC', 'dataUrl' => 'http://sickbeard-xbmc.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://sickbeard-xbmc.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.sickbeard.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://sickbeard-xbmc.googlecode.com/files/repository.sickbeard.xbmc-plugins.zip' ), 
		'Silhouette' => array ( 'name' => 'Silhouette XBMC Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/silhouette2022/kodi/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/silhouette2022/kodi/master/addons.xml', 'repo_id' => 'repository.silhouette', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.silhouette/repository.silhouette-0.zip?raw=true' ),
		'siriuzwhite' => array ( 'name' => 'Siriuz Add-on Repository', 'dataUrl' => 'https://raw.github.com/siriuzwhite/xbmc.repository/master/repository/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/siriuzwhite/xbmc.repository/master/repository/addons.xml', 'repo_id' => 'repository.addons.siriuz', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.addons.siriuz/repository.addons.siriuz-0.zip?raw=true' ),
		'smithgeek' => array( 'name' => 'smithgeek\'s Add-ons', 'dataUrl' => 'https://github.com/brentosmith/xbmc-addons/raw/master/Releases/','statsUrl' => '', 'xmlUrl' => 'https://github.com/brentosmith/xbmc-addons/raw/master/Releases/addons.xml', 'repo_id' => 'repository.smithgeek.xbmc-addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/brentosmith/xbmc-addons/blob/master/repo/repository.smithgeek.xbmc-addons.zip?raw=true' ), 
		'smokdpi' => array( 'name' => 'smokdpi\'s Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/smokdpi/kodi/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/smokdpi/kodi/master/addons.xml', 'repo_id' => 'repository.smokdpi', 'zip' => '1', 'downloadUrl' => 'https://github.com/smokdpi/kodi/blob/master/repository.smokdpi/repository.smokdpi-1.0.0.zip?raw=true' ), 
		'smoothstreams' => array( 'name' => 'SmoothStreams Repo', 'dataUrl' => 'http://cdn.smoothstreams.tv/players/xbmc/repo/','statsUrl' => '', 'xmlUrl' => 'http://smoothstreams.tv/players/xbmc/repo/addons.xml', 'repo_id' => 'repository.smoothstreams', 'zip' => '1', 'downloadUrl' => 'http://cdn.smoothstreams.tv/players/xbmc/repo/repository.smoothstreams/repository.smoothstreams-1.0.2.zip' ), 
		'smuto' => array ( 'name' => 'Polskie wtyczki', 'dataUrl' => 'http://raw.github.com/xbmc-addons-polish/polskie_wtyczki/master/download/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/xbmc-addons-polish/polskie_wtyczki/master/addons.xml', 'repo_id' => 'repository.unofficial.polish', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.unofficial.polish/repository.unofficial.polish-0.zip?raw=true' ),
// Gone		'spacemonkey' => array( 'name' => 'SpaceMonkey\'s Addons', 'dataUrl' => 'http://dl.dropbox.com/u/6561811/Repository/','statsUrl' => '', 'xmlUrl' => 'http://dl.dropbox.com/u/6561811/Repository/addons.xml', 'repo_id' => 'repository.spacemonkey', 'zip' => '1', 'downloadUrl' => 'http://xbmc.aminhacasadigital.com/7-Temas/repository.spacemonkey.zip' ), 
		'sporting streams' => array( 'name' => 'SportingStreams Add-on Repository', 'dataUrl' => 'http://sportingstreams.net/repo/','statsUrl' => '', 'xmlUrl' => 'http://sportingstreams.net/repo/addons.xml', 'repo_id' => '', 'zip' => '', 'downloadUrl' => '' ), 
		'spoyser' => array ( 'name' => 'spoysers XBMC Add-ons', 'dataUrl' => 'https://raw.github.com/spoyser/spoyser-repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/spoyser/spoyser-repo/master/addons.xml', 'repo_id' => 'repository.spoyser', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.spoyser/repository.spoyser-0.zip?raw=true' ),
		'stacked' => array( 'name' => 'stacked Add-on Repository', 'dataUrl' => 'http://plugin.googlecode.com/git/	','statsUrl' => '', 'xmlUrl' => 'http://plugin.googlecode.com/git/addons.xml', 'repo_id' => 'repository.stacked.xbmc.addons', 'zip' => '', 'downloadUrl' => 'https://plugin.googlecode.com/files/repository.stacked.xbmc.addons.zip' ), 
/* addon.xml page not loading */		'steeve' => array ( 'name' => 'Pulsar Repository', 'dataUrl' => 'http://localhost:65251/repository/steeve/','statsUrl' => '', 'xmlUrl' => 'http://localhost:65251/repository/steeve/plugin.video.pulsar/addons.xml', 'repo_id' => 'repository.pulsar', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.pulsar/repository.pulsar-0.zip?raw=true' ),
		'streamstormtv' => array( 'name' => 'streamstorm Addon Repository', 'dataUrl' => 'https://raw.githubusercontent.com/streamstormtv/streamstormtvrepo/master/zips/	','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/streamstormtv/streamstormtvrepo/master/addons.xml', 'repo_id' => 'repository.streamstormtv', 'zip' => '1', 'downloadUrl' => 'https://github.com/streamstormtv/streamstormtvrepo/blob/master/zips/repository.streamstormtv/repository.streamstormtv-1.0.rar?raw=true' ), 
		'Studio-Evolution' => array ( 'name' => 'Studio-Evolution Addons', 'dataUrl' => 'http://raw.github.com/GeekEdem/zip/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/GeekEdem/zip/master/addons.xml', 'repo_id' => 'repository.evolution', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.evolution/repository.evolution-0.zip?raw=true' ),
		'suzuke' => array( 'name' => 'Suzuke Repository', 'dataUrl' => 'https://raw.githubusercontent.com/suzuke/repository.suzuke.xbmc-addons/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/suzuke/repository.suzuke.xbmc-addons/master/addons.xml', 'repo_id' => 'repository.suzuke.xbmc-addons', 'zip' => '1', 'downloadUrl' => '' ), 
		'surmac' => array ( 'name' => 'surmac\'s repo', 'dataUrl' => 'http://bitbucket.org/surmac/surmac-xbmc-repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://bitbucket.org/surmac/surmac-xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.surmac', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.surmac/repository.surmac-0.zip?raw=true' ),
		'syborgs' => array( 'name' => 'Syborg Addon Mods for Skygo', 'dataUrl' => 'http://xbmc-skygo.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-skygo.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.syborg', 'zip' => '1', 'downloadUrl' => 'http://xbmc-skygo.googlecode.com/svn/trunk/addons/repository.syborg/repository.syborg-1.0.2.zip' ), 
		't0mcat' => array( 'name' => 't0mcat Addons', 'dataUrl' => 'http://dl.dropbox.com/u/112011567/xbmc/addons/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
		't0mm0' => array( 'name' => 't0mm0 Addons', 'dataUrl' => 'http://github.com/t0mm0/t0mm0-xbmc-plugins/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://github.com/t0mm0/t0mm0-xbmc-plugins/raw/master/addons.xml', 'repo_id' => 'repository.t0mm0', 'zip' => '1', 'downloadUrl' => 'https://github.com/t0mm0/t0mm0-xbmc-plugins/blob/master/repo/repository.t0mm0/repository.t0mm0-1.0.3.zip?raw=true' ), 
		't0mus' => array( 'name' => 't0mus-xbmc-addons repository', 'dataUrl' => 'http://t0mus-xbmc-addons.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://t0mus-xbmc-addons.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.t0mus', 'zip' => '', 'downloadUrl' => 'http://t0mus-xbmc-addons.googlecode.com/svn/trunk/repository.t0mus-1.0.0.zip' ), 
		'Taxigps' => array ( 'name' => 'Chinese Add-ons', 'dataUrl' => 'https://github.com/taxigps/xbmc-addons-chinese/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/taxigps/xbmc-addons-chinese/raw/master/addons.xml', 'repo_id' => 'repository.xbmc-addons-chinese', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xbmc-addons-chinese/repository.xbmc-addons-chinese-0.zip?raw=true' ),
		'team-expat' => array( 'name' => 'Team eXpat Repo', 'dataUrl' => 'http://raw.github.com/teamexpat/team.expat/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/teamexpat/team.expat/master/addons.xml', 'repo_id' => 'repository.team.expat', 'zip' => '1', 'downloadUrl' => 'https://github.com/teamexpat/team.expat/blob/master/repo/repository.team.expat/repository.team.expat-1.0.5.zip?raw=true' ), 
		'TCSystem(Thomas Goessler)' => array ( 'name' => 'TCSystem KODI Repo', 'dataUrl' => 'http://raw.github.com/ThE-TiGeR/kodi-tcsystem-repository/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/ThE-TiGeR/kodi-tcsystem-repository/master/addons.xml', 'repo_id' => 'repository.tcsystem', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.tcsystem/repository.tcsystem-0.zip?raw=true' ),
		'TDW1980' => array ( 'name' => 'TDW1980 Add-ons', 'dataUrl' => 'https://github.com/tdw1980/tdw/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/tdw1980/tdw/raw/master/addons.xml', 'repo_id' => 'repository.tdw1980', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.tdw1980/repository.tdw1980-0.zip?raw=true' ),
		'Team Wookie' => array ( 'name' => 'Team Wookie Addon Repository', 'dataUrl' => 'http://raw.github.com/metalkettle/Team-Wookie/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/metalkettle/Team-Wookie/master/addons.xml', 'repo_id' => 'repository.wookie', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.wookie/repository.wookie-0.zip?raw=true' ),
		'techdealer' => array ( 'name' => 'Techdealer Repo', 'dataUrl' => 'https://techdealerrepo.svn.codeplex.com/svn/','statsUrl' => '', 'xmlUrl' => 'https://techdealerrepo.svn.codeplex.com/svn/addons.xml', 'repo_id' => 'repository.techdealer', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.techdealer/repository.techdealer-0.zip?raw=true' ),
		'teeedubb' => array ( 'name' => 'teeedubb\'s repo', 'dataUrl' => 'http://raw.github.com/teeedubb/teeedubb-xbmc-repo/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/teeedubb/teeedubb-xbmc-repo/master/addons.xml', 'repo_id' => 'repository.teeedubb', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.teeedubb/repository.teeedubb-0.zip?raw=true' ),
		'teefer' => array( 'name' => 'teefer Add-on Repository', 'dataUrl' => 'http://teefer-xbmc-repo.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://teefer-xbmc-repo.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.teefer.xbmc-plugins', 'zip' => '', 'downloadUrl' => 'https://teefer-xbmc-repo.googlecode.com/files/repository.teefer.xbmc-plugins.zip' ), 
		'TerrorKeed' => array( 'name' => 'Shamzee\'s Repo', 'dataUrl' => 'http://github.com/TerrorKeed/shamzee-repo/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://github.com/TerrorKeed/shamzee-repo/raw/master/addons.xml', 'repo_id' => 'repository.shamzee', 'zip' => '1', 'downloadUrl' => 'https://github.com/TerrorKeed/shamzee-repo/blob/master/zips/repository.shamzee/repository.shamzee-1.0.zip?raw=true' ), 
		'The-One' => array( 'name' => 'The-One\'s Repo', 'dataUrl' => 'http://the-ones-xbmc-repo.googlecode.com/svn/zips/','statsUrl' => '', 'xmlUrl' => 'http://the-ones-xbmc-repo.googlecode.com/svn/addons.xml', 'repo_id' => 'repository.the-one', 'zip' => '1', 'downloadUrl' => 'http://the-ones-xbmc-repo.googlecode.com/svn/zips/repository.the-one/repository.the-one-1.2.zip' ), 
		'the_silencer' => array ( 'name' => 'The_Silencer\'s REPO', 'dataUrl' => 'http://raw.github.com/TheSilencer001/The_Silencer/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/TheSilencer001/The_Silencer/master/addons.xml', 'repo_id' => 'repository.The_Silencer', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.The_Silencer/repository.The_Silencer-0.zip?raw=true' ),
		'TheHighways' => array ( 'name' => 'TheHighway\'s Addons', 'dataUrl' => 'http://raw.github.com/HIGHWAY99/repository.thehighway/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/HIGHWAY99/repository.thehighway/master/addons.xml', 'repo_id' => 'repository.thehighway', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.thehighway/repository.thehighway-0.zip?raw=true' ),
		'TheHighwaysbb' => array( 'name' => 'TheHighway\'s Backup Repo on BitBucket', 'dataUrl' => 'http://bitbucket.org/HIGHWAY99/repository.thehighway.bb/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://bitbucket.org/HIGHWAY99/repository.thehighway.bb/raw/master/addons.bb.xml', 'repo_id' => 'repository.thehighway.bb', 'zip' => '1', 'downloadUrl' => 'https://github.com/HIGHWAY99/repository.thehighway/blob/master/repo/repository.TheHighwaysEasyInstallRepo/repository.TheHighwaysEasyInstallRepo-0.0.1.zip?raw=true' ), 
		'TheHighway' => array ( 'name' => 'TheHighway\'s Broken and Outdated Addons', 'dataUrl' => 'http://raw.github.com/HIGHWAY99/repository.thehighway.br/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/HIGHWAY99/repository.thehighway.br/master/addons.xml', 'repo_id' => 'repository.thehighway.br', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.thehighway.br/repository.thehighway.br-0.zip?raw=true' ),
		'TheHighwaysEasyInstall' => array( 'name' => 'TheHighway\'s Easy Install Repo', 'dataUrl' => 'http://raw.github.com/HIGHWAY99/repository.thehighway/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://github.com/HIGHWAY99/repository.thehighway/raw/master/repoEasyInstall.xml', 'repo_id' => 'repository.TheHighwaysEasyInstallRepo', 'zip' => '1', 'downloadUrl' => 'https://github.com/HIGHWAY99/repository.thehighway/blob/master/repo/repository.TheHighwaysEasyInstallRepo/repository.TheHighwaysEasyInstallRepo-0.0.1.zip?raw=true' ), 
		'TheWiz' => array ( 'name' => 'TheWiz Hebrew Repository', 'dataUrl' => 'http://repo.thewiz.info/','statsUrl' => '', 'xmlUrl' => 'http://repo.thewiz.info/addons.xml', 'repo_id' => 'repository.TheWiz', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.TheWiz/repository.TheWiz-0.zip?raw=true' ),
// Other is the newer one but showing blank in browser		'TheWiz' => array( 'name' => 'TheWiz Hebrew Repo', 'dataUrl' => 'http://thewiz.info/XBMC/','statsUrl' => '', 'xmlUrl' => 'http://thewiz.co.il/xbmc/addons.xml', 'repo_id' => 'repository.TheWiz', 'zip' => '1', 'downloadUrl' => '' ), 
		'TheYid' => array( 'name' => 'TheYid Repo', 'dataUrl' => 'https://raw.githubusercontent.com/TheYid/My-Repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/TheYid/My-Repo/master/addons.xml', 'repo_id' => 'repository.TheYid', 'zip' => '1', 'downloadUrl' => 'https://github.com/TheYid/My-Repo/blob/master/zips/repository.TheYid/repository.TheYid-1.5.zip?raw=true' ), 
		'ThongLD' => array( 'name' => 'ThongLD`s REPO', 'dataUrl' => 'http://echipstore.net/thongld/','statsUrl' => '', 'xmlUrl' => 'http://echipstore.net/thongld/addons.xml', 'repo_id' => 'repository.thongld', 'zip' => '1', 'downloadUrl' => 'http://echipstore.net/thongld/repository.thongld/repository.thongld-1.0.zip' ), 
		'THN' => array( 'name' => 'THN\'s Addons', 'dataUrl' => 'http://repothn.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://repothn.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.repothn', 'zip' => '', 'downloadUrl' => 'https://repothn.googlecode.com/files/repository.googlecode.repothn.zip' ), 
		'tkantor81' => array( 'name' => 'tkantor81\'s Addons', 'dataUrl' => 'https://raw.githubusercontent.com/tkantor81/repository.tkantor81/master/repository/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/tkantor81/repository.tkantor81/master/repository/addons.xml', 'repo_id' => 'repository.tkantor81', 'zip' => '1', 'downloadUrl' => '' ), 
		'tknorris' => array( 'name' => 'tknorris Beta Testing Repository', 'dataUrl' => 'https://github.com/tknorris/tknorris-beta-repo/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/tknorris/tknorris-beta-repo/raw/master/addons.xml', 'repo_id' => 'repository.tknorris.beta', 'zip' => '1', 'downloadUrl' => 'https://github.com/tknorris/tknorris-beta-repo/blob/master/zips/repository.tknorris.beta/repository.tknorris.beta-1.0.5.zip?raw=true' ), 
		'tknorrisrelease' => array( 'name' => 'tknorris Release Repository', 'dataUrl' => 'https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/addons.xml', 'repo_id' => 'repository.tknorris.release', 'zip' => '1', 'downloadUrl' => 'https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/zips/repository.tknorris.release/repository.tknorris.release-1.0.1.zip' ), 
		'TLBB' => array ( 'name' => 'TLBB Repository', 'dataUrl' => 'http://cloud.thelittleblackbox.co.uk/repo/zips/','statsUrl' => '', 'xmlUrl' => 'http://cloud.thelittleblackbox.co.uk/repo/addons.xml', 'repo_id' => 'repository.tlbb', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.tlbb/repository.tlbb-0.zip?raw=true' ),
		'todits' => array ( 'name' => 'todits.xbmc Add-ons', 'dataUrl' => 'https://github.com/todits-xbmc/todits-xbmc-tv/raw/master/downloads/','statsUrl' => '', 'xmlUrl' => 'https://github.com/todits-xbmc/todits-xbmc-tv/raw/master/addons.xml', 'repo_id' => 'repository.todits.xbmc.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.todits.xbmc.addons/repository.todits.xbmc.addons-0.zip?raw=true' ),
		'tolin' => array( 'name' => 'TOLIN XBMC Add-on\'s', 'dataUrl' => 'http://tolin-xbmc-repo.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://tolin-xbmc-repo.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.tolin', 'zip' => '', 'downloadUrl' => 'https://tolin-xbmc-repo.googlecode.com/svn/trunk/repository.tolin.zip' ), 
		'Topklassetv' => array( 'name' => 'Topklasse TV Repository', 'dataUrl' => 'http://clubtv.dooremolen.com/topklasse/addons/','statsUrl' => '', 'xmlUrl' => 'http://clubtv.dooremolen.com/topklasse/addons/addons.xml', 'repo_id' => 'repository.repository.topklassetv', 'zip' => '1', 'downloadUrl' => 'http://clubtv.dooremolen.com/topklasse/addons/repository.topklassetv/repository.topklassetv.zip' ), 
// Gone		'totalinstaller' => array( 'name' => 'Total Installer Repo', 'dataUrl' => 'https://raw.github.com/totalxbmc/totalinstaller/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://github.com/totalxbmc/totalinstaller/raw/master/zips/addons.xml', 'repo_id' => 'repository.totalinstaller', 'zip' => '1', 'downloadUrl' => 'https://github.com/totalxbmc/totalinstaller/blob/master/zips/repository.totalinstaller/repository.totalinstaller-1.0.1.zip?raw=true' ), 
		'traitravinh' => array ( 'name' => 'TraiTraVinh\'s Testing Repo', 'dataUrl' => 'https://raw.github.com/traitravinh/traitravinh.repository.xbmc/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/traitravinh/traitravinh.repository.xbmc/master/addons.xml', 'repo_id' => 'repository.traitravinh', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.traitravinh/repository.traitravinh-0.zip?raw=true' ),
		'tugafree' => array( 'name' => 'Tugafree Repositorio', 'dataUrl' => 'http://raw.github.com/Tugafree/Tugafree.repositorio/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/Tugafree/Tugafree.repositorio/master/addons.xml', 'repo_id' => 'Tugafree.repositorio', 'zip' => '1', 'downloadUrl' => 'https://github.com/Tugafree/Tugafree.repositorio/blob/master/repo/Tugafree.repositorio/Tugafree.repositorio-0.0.4.zip?raw=true' ), 
		'TVAddons.nl' => array ( 'name' => '.TV Addons Nederland', 'dataUrl' => 'http://repo.tvaddons.nl/repo/','statsUrl' => '', 'xmlUrl' => 'http://repo.tvaddons.nl/addons.xml', 'repo_id' => 'repository.tvaddons.nl', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.tvaddons.nl/repository.tvaddons.nl-0.zip?raw=true' ),
/* website down	*/	'TVCatchup' => array( 'name' => 'TVCatchup Repository', 'dataUrl' => 'http://plugins.tvcatchup.com/~xbmc/addons/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => 'repository.tvcatchup.addons', 'zip' => '1', 'downloadUrl' => '' ), 
		'TVChinese' => array( 'name' => 'TVChinese Add-on Repository', 'dataUrl' => 'hhttp://xbmc-addon-tv-tianxianbaby.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-addon-tv-tianxianbaby.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-addon-txbb', 'zip' => '', 'downloadUrl' => 'https://xbmc-addon-tv-tianxianbaby.googlecode.com/files/repository.googlecode.xbmc-addon-txbb.zip' ), 
		'TvM' => array( 'name' => 'TvM Add-ons', 'dataUrl' => 'http://repository-xbmc-tvm.googlecode.com/git/','statsUrl' => '', 'xmlUrl' => 'http://repository-xbmc-tvm.googlecode.com/git/addons.xml', 'repo_id' => 'repository.xbmc.tvm', 'zip' => '1', 'downloadUrl' => 'http://repository-xbmc-tvm.googlecode.com/git/repository.xbmc.tvm/repository.xbmc.tvm-1.0.zip' ), 
		'TVShack' => array( 'name' => 'TVShack Repo', 'dataUrl' => 'http://xbmc-tvshack.googlecode.com/svn/branches/DHARMA/repo/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-tvshack.googlecode.com/svn/branches/DHARMA/repo/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-tvshack', 'zip' => '', 'downloadUrl' => 'http://xbmc-tvshack.googlecode.com/svn/branches/DHARMA/repo/repository.googlecode.xbmc-tvshack.zip' ),
		'twitxbmc' => array( 'name' => 'XBMC Eraser\'s Addons', 'dataUrl' => 'http://twitxbmc.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://twitxbmc.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.eraser', 'zip' => '', 'downloadUrl' => 'http://twitxbmc.googlecode.com/svn/addons/repository.eraser.zip' ),
		'twinther' => array( 'name' => 'twinther\'s beta repository', 'dataUrl' => 'http://tommy.winther.nu/xbmc/','statsUrl' => '', 'xmlUrl' => 'http://tommy.winther.nu/xbmc/addons.xml', 'repo_id' => 'repository.twinther', 'zip' => '1', 'downloadUrl' => 'http://tommy.winther.nu/xbmc/zip.php?addon=repository.twinther' ),
		'unofficial_addon_pro' => array( 'name' => 'Unofficial OpenELEC (WeTek_Play/arm) Add-ons', 'dataUrl' => 'http://unofficial.addon.pro/addons/4.3/WeTek_Play/arm/','statsUrl' => '', 'xmlUrl' => 'http://unofficial.addon.pro/addons/4.3/WeTek_Play/arm/addons.xml', 'repo_id' => 'repository.unofficial.addon.pro', 'zip' => '1', 'downloadUrl' => '' ), 
		'uplayhd' => array( 'name' => 'uPlayHD XBMC Add-ons', 'dataUrl' => 'http://bitbucket.org/iClosedz/uplayhd-xbmc-addons/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://bitbucket.org/iClosedz/uplayhd-xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.uplayhd', 'zip' => '1', 'downloadUrl' => 'https://github.com/iClosedz/uPlayHD-xbmc-addons/blob/master/repository.uplayhd/repository.uplayhd.zip?raw=true' ), 
		'VODie' => array( 'name' => 'xbmc-vodie Add-ons', 'dataUrl' => 'http://xbmc-vodie.googlecode.com/svn/repo/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-vodie.googlecode.com/svn/repo/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-vodie', 'zip' => '1', 'downloadUrl' => 'http://xbmc-vodie.googlecode.com/svn/repo/repository.googlecode.xbmc-vodie/repository.googlecode.xbmc-vodie-1.0.1.zip' ), 
		'VEOLO' => array( 'name' => 'VEOLO Add-ons', 'dataUrl' => 'https://copy.com/3ZP97S79haAMs0IF/Repo.VEOLO/addons/','statsUrl' => '', 'xmlUrl' => 'https://copy.com/3ZP97S79haAMs0IF/Repo.VEOLO/addons.xml', 'repo_id' => 'repository.VEOLO', 'zip' => '1', 'downloadUrl' => 'https://copy.com/3ZP97S79haAMs0IF/Repo.VEOLO/addons/repository.VEOLO' ), 
		'VEOLOUnofficial' => array( 'name' => 'VEOLO Unofficial Add-on Repository', 'dataUrl' => 'https://copy.com/28Xcy7CVHIikzfq6/Repo.VEOLO.Unofficial/addons/','statsUrl' => '', 'xmlUrl' => 'https://copy.com/28Xcy7CVHIikzfq6/Repo.VEOLO.Unofficial/addons.xml', 'repo_id' => 'repository.VEOLO.Unofficial', 'zip' => '1', 'downloadUrl' => 'https://copy.com/28Xcy7CVHIikzfq6/Repo.VEOLO.Unofficial/addons/repository.VEOLO.Unofficial' ), 
		'VietMedia' => array ( 'name' => 'repository.vietmedia', 'dataUrl' => 'https://raw.github.com/onepas/kodi-addons/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/onepas/kodi-addons/master/addons.xml', 'repo_id' => 'repository.vietmedia', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.vietmedia/repository.vietmedia-0.zip?raw=true' ),
		'VinmanJSV' => array( 'name' => 'VinmanJSV REPO', 'dataUrl' => 'https://github.com/VinmanJSV/OPENJAVA/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/VinmanJSV/OPENJAVA/master/addons.xml', 'repo_id' => 'repository.VinManJSV', 'zip' => '1', 'downloadUrl' => 'https://github.com/VinmanJSV/OPENJAVA/raw/master/zips/repository.VinManJSV/repository.VinManJSV-1.1.zip' ), 
		'vinnydude' => array ( 'name' => 'Addons by Vinnydude', 'dataUrl' => 'http://raw.github.com/vinnydude/vinnydude.repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/vinnydude/vinnydude.repo/master/addons.xml', 'repo_id' => 'repository.Vinnydude', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.Vinnydude/repository.Vinnydude-0.zip?raw=true' ),
		'voinage' => array( 'name' => 'Voinage Add-ons', 'dataUrl' => 'https://voinage-xbmc-plugins.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'https://voinage-xbmc-plugins.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.voinage', 'zip' => '', 'downloadUrl' => 'https://voinage-xbmc-plugins.googlecode.com/files/repository.voinage.zip' ), 
		'vstream' => array( 'name' => 'vStream Repository', 'dataUrl' => 'https://github.com/LordVenom/venom-xbmc-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/addons.xml', 'repo_id' => 'repository.vstream', 'zip' => '1', 'downloadUrl' => 'https://github.com/LordVenom/venom-xbmc-addons/blob/master/repo/repository.vstream/repository.vstream.zip?raw=true' ), 
		'wareztuga' => array( 'name' => 'Wareztuga TV Repository', 'dataUrl' => 'http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/','statsUrl' => '', 'xmlUrl' => 'http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/addons.xml', 'repo_id' => 'repository.wareztuga/repository.wareztuga', 'zip' => '1', 'downloadUrl' => '' ), 
		'whitecream' => array( 'name' => 'Whitecream Repository', 'dataUrl' => 'http://whitecream.googlecode.com/svn/trunk/addon/','statsUrl' => '', 'xmlUrl' => 'http://whitecream.googlecode.com/svn/trunk/addon/addons.xml', 'repo_id' => 'repository.0whitecream0', 'zip' => '1', 'downloadUrl' => 'http://whitecream.googlecode.com/svn/trunk/addon/repository.0whitecream0/repository.0whitecream0-1.0.0.zip' ), 
		'wiiego' => array( 'name' => 'Wiiego Add-ons', 'dataUrl' => 'https://github.com/diegofn/wiiego-xbmc-addons/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/diegofn/wiiego-xbmc-addons/raw/master/addons.xml', 'repo_id' => 'repository.wiiego', 'zip' => '1', 'downloadUrl' => 'https://github.com/diegofn/wiiego-xbmc-addons/blob/master/repo/repository.wiiego/repository.wiiego-1.0.1.zip?raw=true' ), 
		'wliptv' => array( 'name' => 'WLIPTV Repository', 'dataUrl' => 'http://xbmc.wliptv.com/','statsUrl' => '', 'xmlUrl' => 'http://xbmc.wliptv.com/addons.xml', 'repo_id' => 'repository.wliptv', 'zip' => '1', 'downloadUrl' => 'http://xbmc.wliptv.com/repository.wliptv/repository.wliptv-0.0.3.zip' ), 
		'WolfTeam' => array ( 'name' => 'Wolf-Team official Repo', 'dataUrl' => 'https://svn.code.sf.net/u/teamwolf/code/addons/','statsUrl' => '', 'xmlUrl' => 'https://svn.code.sf.net/u/teamwolf/code/addons/addons.xml', 'repo_id' => 'repository.wolf-team', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.wolf-team/repository.wolf-team-0.zip?raw=true' ),
		'xb-israel' => array( 'name' => 'xb-israel, israeli VOD', 'dataUrl' => 'http://xb-israel.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://xb-israel.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.xb-israel.shmulik', 'zip' => '', 'downloadUrl' => 'https://xb-israel.googlecode.com/files/repository.xb-israel.shmulik.zip' ), 
		'xbmc-czech' => array( 'name' => 'Czech Add-ons', 'dataUrl' => 'http://xbmc-czech.sf.net/addons/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-czech.sf.net/addons/addons.xml', 'repo_id' => 'repository.xbmc-czech.sf.net', 'zip' => '1', 'downloadUrl' => 'http://xbmc-czech.sourceforge.net/addons/repository.xbmc-czech.sf.net/repository.xbmc-czech.sf.net-1.0.zip' ), 
		'xbmc-israel' => array( 'name' => 'XBMC Israeli Streaming Sites', 'dataUrl' => 'https://raw.githubusercontent.com/cubicle-vdo/xbmc-israel/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/cubicle-vdo/xbmc-israel/raw/master/addons.xml', 'repo_id' => 'repository.xbmc-israel', 'zip' => '1', 'downloadUrl' => 'https://github.com/cubicle-vdo/xbmc-israel/blob/master/repo/repository.xbmc-israel/repository.xbmc-israel-1.0.4.zip?raw=true' ), 
		'xbmc-korea-frodo' => array( 'name' => 'XBMC Korea Add-ons', 'dataUrl' => 'http://xbmc-korea-addons.googlecode.com/svn/addons/frodo/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-korea-addons.googlecode.com/svn/addons/frodo/addons.xml', 'repo_id' => 'repository.xbmc-korea.com', 'zip' => '1', 'downloadUrl' => 'https://xbmc-korea-addons.googlecode.com/files/repository.xbmc-korea.com-1.0.6.zip' ), 
		'xbmc-korea-gotham' => array( 'name' => 'XBMC Korea Add-ons', 'dataUrl' => 'http://xbmc-korea-addons.googlecode.com/svn/addons/gotham/','statsUrl' => '', 'xmlUrl' => 'http://xbmc-korea-addons.googlecode.com/svn/addons/gotham/addons.xml', 'repo_id' => 'repository.xbmc-korea.com', 'zip' => '1', 'downloadUrl' => 'https://xbmc-korea-addons.googlecode.com/files/repository.xbmc-korea.com-1.0.7.zip' ), 
		'xbmc-palestine' => array( 'name' => 'XBMC palestine streaming repo for streaming sites', 'dataUrl' => 'https://raw.githubusercontent.com/yosir/xbmc-pal/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/yosir/xbmc-pal/raw/master/addons.xml', 'repo_id' => 'repository.xbmc-pal', 'zip' => '1', 'downloadUrl' => 'https://github.com/yosir/xbmc-pal/blob/master/repo/repository.xbmc-pal/repository.xbmc-pal-1.6.0.zip?raw=true' ), 
/* removed */		'xbmc-skin-development' => array( 'name' => 'XBMC.org Skin Development Repository', 'dataUrl' => 'http://mirrors.xbmc.org/addons/gotham-skins-staging/','statsUrl' => '', 'xmlUrl' => '', 'repo_id' => 'repository.xbmc.skins.staging', 'zip' => '1', 'downloadUrl' => '' ), 
		'xbmcadult' => array ( 'name' => 'XBMC-Adult Addons', 'dataUrl' => 'http://raw.github.com/xbmc-adult/xbmc-adult/ghmaster/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/xbmc-adult/xbmc-adult/ghmaster/addons.xml', 'repo_id' => 'repository.xbmcadult', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xbmcadult/repository.xbmcadult-0.zip?raw=true' ),
		'XBMCCatchupTVAU' => array( 'name' => 'XBMC CatchupTV AU Add-on Repository', 'dataUrl' => 'https://github.com/xbmc-catchuptv-au/repo/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/xbmc-catchuptv-au/repo/master/addons.xml', 'repo_id' => 'repository.googlecode.xbmc-catchuptv-au', 'zip' => '1', 'downloadUrl' => 'https://github.com/xbmc-catchuptv-au/repo/blob/master/repository.googlecode.xbmc-catchuptv-au/repository.googlecode.xbmc-catchuptv-au-1.3.zip?raw=true' ), 
/* Blank */		'xbmcnerdsFrodo' => array ( 'name' => 'xbmcnerds.com Add-ons (Frodo)', 'dataUrl' => 'http://repodl.xbmcnerds.com/repository/frodo/','statsUrl' => '', 'xmlUrl' => 'http://repodl.xbmcnerds.com/repository/frodo/addons.xml', 'repo_id' => 'repository.xbmcnerds.frodo', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xbmcnerds.frodo/repository.xbmcnerds.frodo-0.zip?raw=true' ),
		'xbmcnerdsGotham' => array( 'name' => 'kodinerds.net Add-ons (Gotham)', 'dataUrl' => 'http://repo.skinquantum.de/repo/','statsUrl' => '', 'xmlUrl' => 'http://repo.skinquantum.de/repo/addons.xml', 'repo_id' => 'repository.xbmcnerds', 'zip' => '1', 'downloadUrl' => '' ), 
		'xbmcnerdsHelix' => array( 'name' => 'kodinerds.net Add-ons (Helix)', 'dataUrl' => 'http://repo.skinquantum.de/nerdsrepo/helix/','statsUrl' => '', 'xmlUrl' => 'http://repo.skinquantum.de/nerdsrepo/helix/addons.xml', 'repo_id' => 'repository.kodinerds.helix', 'zip' => '1', 'downloadUrl' => '' ), 
		'xbmcplus' => array( 'name' => 'xbmcplus Add-on Repository', 'dataUrl' => 'https://raw.githubusercontent.com/moneymaker365/xbmc-xbmcplus-plugins/master/download/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/moneymaker365/xbmc-xbmcplus-plugins/master/addons.xml', 'repo_id' => 'repository.xbmcplus.xbmc-plugins', 'zip' => '1', 'downloadUrl' => 'https://github.com/moneymaker365/xbmc-xbmcplus-plugins/blob/master/download/repository.xbmcplus.xbmc-plugins/repository.xbmcplus.xbmc-plugins-1.4.zip?raw=true' ), 
		'xbmcru.db' => array ( 'name' => 'xbmc.ru search.db Repo', 'dataUrl' => 'https://github.com/seppius-xbmc-repo/ru/raw/master/','statsUrl' => '', 'xmlUrl' => 'https://github.com/seppius-xbmc-repo/ru/raw/master/addons.xml', 'repo_id' => 'repository.search.db', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.search.db/repository.search.db-0.zip?raw=true' ),
		'xhaggi' => array ( 'name' => 'xhaggi\'s repository', 'dataUrl' => 'https://raw.githubusercontent.com/xhaggi/kodi-addons/master/data/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/xhaggi/kodi-addons/master/addons.xml', 'repo_id' => 'repository.xhaggi', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xhaggi/repository.xhaggi-0.zip?raw=true' ),
		'xlordx' => array( 'name' => 'XLordKX Repo', 'dataUrl' => 'https://raw.githubusercontent.com/XLordKX/kodi/master/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/XLordKX/kodi/master/addons.xml', 'repo_id' => 'repository.xlordkx', 'zip' => '1', 'downloadUrl' => 'https://raw.githubusercontent.com/XLordKX/kodi/master/zip/repository.xlordkx/repository.xlordkx-1.0.0.zip' ), 
		'xsteal' => array ( 'name' => 'xsteal repository', 'dataUrl' => 'http://raw.github.com/xsteal/repository.xsteal/master/repo/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/xsteal/repository.xsteal/master/addons.xml', 'repo_id' => 'repository.xsteal', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.xsteal/repository.xsteal-0.zip?raw=true' ),
		'xunitytalk' => array( 'name' => 'xunitytalk Repository', 'dataUrl' => 'http://xty.me/xunitytalk/addons/','statsUrl' => '', 'xmlUrl' => 'http://xty.me/xunitytalk/addons/addons.xml', 'repo_id' => 'repository.xunitytalk', 'zip' => '1', 'downloadUrl' => 'http://xunitytalk.com/xfinity/XunityTalk_Repository.zip' ), 
		'xycl' => array( 'name' => 'xycl Add-ons', 'dataUrl' => 'https://raw.github.com/Xycl/repository.xycl.addons/master/','statsUrl' => '', 'xmlUrl' => 'https://raw.github.com/Xycl/repository.xycl.addons/master/addons.xml', 'repo_id' => 'repository.xycl.addons', 'zip' => '1', 'downloadUrl' => 'https://github.com/Xycl/repository.xycl.addons/blob/master/repository.xycl.addons/repository.xycl.addons-1.2.1.zip?raw=true' ),
		'yllar' => array ( 'name' => 'Yllar\'s XBMC Addons', 'dataUrl' => 'https://github.com/yllar/yllar-xbmc-repo/raw/master/repo/','statsUrl' => '', 'xmlUrl' => 'https://github.com/yllar/yllar-xbmc-repo/raw/master/addons.xml', 'repo_id' => 'repository.yllar', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.yllar/repository.yllar-0.zip?raw=true' ),
		'YoshioftheWire' => array( 'name' => 'urlXL XBMC Addon Repo', 'dataUrl' => 'https://github.com/totalinstall/manual-updates/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://urlxl-repo.googlecode.com/git/addons.xml', 'repo_id' => '', 'zip' => '', 'downloadUrl' => '' ), 
		'zeus' => array ( 'name' => 'ZEUS Repository', 'dataUrl' => 'http://repo.zeusrepo.com/zips/','statsUrl' => '', 'xmlUrl' => 'http://repo.zeusrepo.com/addons.xml', 'repo_id' => 'repository.zeus', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.zeus/repository.zeus-0.zip?raw=true' ),
// Gone		'ztas' => array( 'name' => 'Zatz addons', 'dataUrl' => 'http://ztas-xbmc-addons.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://ztas-xbmc-addons.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.ztas', 'zip' => '', 'downloadUrl' => 'https://ztas-xbmc-addons.googlecode.com/files/repository.ztas.zip' ), 
/*not working for some reason */		'xtream' => array( 'name' => 'Xtream Media add-on repository', 'dataUrl' => 'http://xtream-media.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://xtream-media.googlecode.com/svn/addons/addons.xml', 'repo_id' => 'repository.googlecode.XtreamMedia', 'zip' => '1', 'downloadUrl' => 'https://xtream-media.googlecode.com/files/repository.googlecode.xtream-media.zip' ), 

//other repositories
		'openelec' => array( 'name' => 'OpenElec Add-Ons', 'dataUrl' => 'http://unofficial.addon.pro/addons/3.1/RPi/arm/','statsUrl' => '', 'xmlUrl' => 'http://unofficial.addon.pro/addons/3.1/RPi/arm/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 

//need to add to manual		'jas0npc' => array( 'name' => 'Jas0nPC\'s Repo', 'dataUrl' => 'https://bitbucket.org/jas0npc_13/jas0npc-repo/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://bitbucket.org/jas0npc_13/jas0npc-repo/raw/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/jas0npc/jas0npc/blob/master/zips/repository.Jas0npc/repository.Jas0npc-1.6.zip?raw=true' ),
//now private		'dudehere' => array( 'name' => 'dudehere Repo', 'dataUrl' => 'https://dudehere-repository.googlecode.com/git/addons/','statsUrl' => '', 'xmlUrl' => 'https://dudehere-repository.googlecode.com/git/addons/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/dudehere5/repository.dudehere.plugins/blob/master/repository.dudehere.plugins-1.0.2.zip?raw=true' ), 
//repo has been deleted		'horizon0156' => array( 'name' => 'Horizon777 XBMC Add-ons', 'dataUrl' => 'https://raw.githubusercontent.com/Horizon0156/repository.horizon.xbmc/master/zip/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/Horizon0156/repository.horizon.xbmc/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/Horizon0156/repository.horizon.xbmc/blob/master/zip/repository.horizon.xbmc/repository.horizon.xbmc-1.0.zip?raw=true' )
//just contains others work		'pampereo' => array( 'name' => 'Pampereo XBMC Add-on Repository', 'dataUrl' => 'http://pampereo-xbmc-plugins.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://pampereo-xbmc-plugins.googlecode.com/svn/trunk/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://pampereo-xbmc-plugins.googlecode.com/svn/Zip/repository.pampereo.xbmc-addons.zip' ), 
//backup repo		'dk-XBMC-repository' => array( 'name' => 'dk-xbmc-repaddon Add-on Repository', 'dataUrl' => 'http://162.248.143.235/xbmc/','statsUrl' => '', 'xmlUrl' => 'http://162.248.143.235/xbmc/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'http://162.248.143.235/xbmc/repository.dk-xbmc-repaddon.zip' ), 
//seems to have vanished	'casual' => array( 'name' => 'Team Jacker', 'dataUrl' => 'http://aur.causal.ca/xbmc/addons/','statsUrl' => '', 'xmlUrl' => 'http://aur.causal.ca/xbmc/addons/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'http://aur.causal.ca/xbmc/addons/repository.causal.ca/repository.causal.ca-2.1.0.zip' ), 
//empty repo		'xbxl' => array( 'name' => 'The Xbxl Add-on Repository', 'dataUrl' => 'https://xbmc-dpstream.googlecode.com/git/repository/','statsUrl' => '', 'xmlUrl' => 'https://xbmc-dpstream.googlecode.com/git/repository/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://xbmc-dpstream.googlecode.com/files/repository.xbxl.zip' ), 
//now in official repo		'urlxl' => array( 'name' => 'urlXL Add-on Repository', 'dataUrl' => 'https://github.com/totalinstall/manual-updates/raw/master/','statsUrl' => '', 'xmlUrl' => 'http://urlxl-repo.googlecode.com/git/gotham/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://drive.google.com/file/d/0B3jP6FXjlDKTcWwzUl9kMU02VUE/edit' ), 
//on main xbmc repo and own repo is just wip		'twinther' => array( 'name' => 'twinther Add-ons', 'dataUrl' => 'http://tommy.winther.nu/xbmc/','statsUrl' => '', 'xmlUrl' => 'http://tommy.winther.nu/xbmc/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
//seems to have disappeared	'StreamOn' => array( 'name' => 'StreamOn Repository', 'dataUrl' => 'https://dl.dropbox.com/u/57491593/repo1/','statsUrl' => '', 'xmlUrl' => 'https://dl.dropbox.com/u/57491593/repo1/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
//password protected		'enen92' => array( 'name' => 'MovK Add-on Repository', 'dataUrl' => 'http://movk-xbmc-addon.googlecode.com/svn/','statsUrl' => '', 'xmlUrl' => 'http://movk-xbmc-addon.googlecode.com/svn/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => '' ), 
//password protected		'carb0s' => array( 'name' => 'carb0\'s Repo', 'dataUrl' => 'http://carb0s-repo.googlecode.com/svn/addons/','statsUrl' => '', 'xmlUrl' => 'http://carb0s-repo.googlecode.com/svn/addons/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'http://carb0s-repo.googlecode.com/svn/repository.carb0s.zip' ), 
//deleted		'TheYidXXX' => array( 'name' => 'TheYid XXX Repo', 'dataUrl' => 'https://raw.githubusercontent.com/TheYid/My-Repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://bitbucket.org/tcz009/theyidxxx/raw/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/TheYid/My-Repo/blob/master/zips/repository.TheYidXXX/repository.TheYidXXX-1.4.zip?raw=true' ), 
//shut down DMCA	'cocawe' => array( 'name' => 'Cocawe\'s Add-on Repository', 'dataUrl' => 'https://raw.github.com/cocawe/My-xbmc-repo/master/zips/','statsUrl' => '', 'xmlUrl' => 'https://raw.githubusercontent.com/cocawe/My-xbmc-repo/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/cocawe/My-xbmc-repo/blob/master/zips/repository.cocawe/repository.cocawe-1.3.zip?raw=true' ), 
//Repo Taken down DMCA		'sportsdevil' => array( 'name' => 'SportsDevil Repository', 'dataUrl' => 'http://raw.github.com/al101/repository.SportsDevil/master/','statsUrl' => '', 'xmlUrl' => 'http://raw.github.com/al101/repository.SportsDevil/master/addons.xml', 'repo_id' => '', 'zip' => '1', 'downloadUrl' => 'https://github.com/al101/repository.SportsDevil/blob/master/repository.SportsDevil/repository.SportsDevil-1.0.1.zip?raw=true' ), 
//taken down DCMA		'Mash2k3' => array ( 'name' => 'All Addons by Mash2k3', 'dataUrl' => 'http://bitbucket.org/mash2k3/mash2k3-repository/raw/master/zips/','statsUrl' => '', 'xmlUrl' => 'http://bitbucket.org/mash2k3/mash2k3-repository/raw/master/addons.xml', 'repo_id' => 'repository.mash2k3', 'zip' => '1', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.mash2k3/repository.mash2k3-0.zip?raw=true' ),
//Has duplicate mainbranch addons		'xbmc4xbox' => array( 'name' => 'XBMC-4-XBOX Addon Repository','dataUrl' => 'http://addons4xbox.googlecode.com/svn/trunk/','xmlUrl' => 'http://addons4xbox.googlecode.com/svn/trunk/addons.xml','repo_id' => '', 'zip' => '1','downloadUrl' => ''),
		'eleazar_bak' => array(
			'name' => 'eleazar Repo',
			'dataUrl' => 'https://offshoregit.com/eleazarcoding/eleazar-xbmc/raw/master/',
			'statsUrl' => '',
			'xmlUrl' => 'http://totalxbmc.tv/addons/backuprepos/eleazaraddons.xml',
			'repo_id' => 'repository.eleazar',
			'zip' => '1',
			'downloadUrl' => 'https://offshoregit.com/eleazarcoding/eleazar-xbmc/raw/master/repository.eleazar/repository.eleazar-1.3.zip'
		), 
		'blazetamer_bak' => array(
			'name' => 'BlazeTamer Repo',
			'dataUrl' => 'http://offshoregit.com/Blazetamer/repo/raw/master/zips/',
			'xmlUrl' => 'http://noobsandnerds.com/addons/backuprepos/blazeaddons.xml',
			'repo_id' => 'repository.BlazeRepo',
			'zip' => '1',
			'statsUrl' => '',
			'downloadUrl' => 'https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo/repository.BlazeRepo-3.0.zip'
		),
		'tknorrisrelease_bak' => array(
			'name' => 'tknorris Release Repository',
			'dataUrl' => 'https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/zips/',
			'xmlUrl' => 'http://noobsandnerds.com/addons/backuprepos/tknorrisrelease.xml',
			'repo_id' => 'repository.tknorris.release',
			'zip' => '1',
			'statsUrl' => '',
			'downloadUrl' => 'https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/zips/repository.tknorris.release/repository.tknorris.release-1.0.1.zip'
		),
        'tvaddons_bak' => array(
			'name' => 'TVADDONS.ag Addon Repository',
			'dataUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/',
			'xmlUrl' => 'http://noobsandnerds.com/addons/backuprepos/hubaddons.xml',
			'repo_id' => 'repository.xbmchub',
			'zip' => '1',
			'statsUrl' => '',
			'downloadUrl' => 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.6.zip'
		),
//contains others work as well
		'OpenELEQ' => array( 'name' => 'OpenELEQ Add-ons', 'dataUrl' => 'https://copy.com/KUhv9ZWme2BkoLD3/Repo/addons/','statsUrl' => '', 'xmlUrl' => 'https://archive.org/download/OpenELEQ/openeleq-addons.xml', 'repo_id' => 'repository.openeleq', 'zip' => '1', 'downloadUrl' => 'http://archive.org/download/OpenELEQ/repository.openeleq.zip' ), 
		'ditistv' => array( 'name' => 'DITisTV Repository', 'dataUrl' => 'http://addons.ditistv.nl/repo/', 'statsUrl' => '', 'xmlUrl' => 'http://addons.ditistv.nl/addons.xml', 'repo_id' => 'repository.ditistv', 'zip' => '1', 'downloadUrl' => '' ), 
		'iamfreetofly' => array ( 'name' => 'iamfreetofly Add-on Repository', 'dataUrl' => 'http://iamfreetofly-xbmc-repaddon.googlecode.com/svn/trunk/','statsUrl' => '', 'xmlUrl' => 'http://iamfreetofly-xbmc-repaddon.googlecode.com/svn/trunk/addons.xml', 'repo_id' => 'repository.iamfreetofly-xbmc-repaddon', 'zip' => '0', 'downloadUrl' => 'https://github.com/noobsandnerds/noobsandnerds/blob/master/repository.iamfreetofly-xbmc-repaddon/repository.iamfreetofly-xbmc-repaddon-0.zip?raw=true' ),
		'superrepo' => array( 'name' => 'SuperRepo  All', 'dataUrl' => 'http://redirect.superrepo.org/v5/addons/','statsUrl' => '', 'xmlUrl' => 'http://xml.superrepo.org/v5/.xml/helix/all/addons.xml', 'repo_id' => 'repository.superrepo.org.helix.all', 'zip' => '1', 'downloadUrl' => '' ),
		'kozz' => array( 'name' => 'Kozz Add-ons', 'dataUrl' => 'http://kozz-addons.googlecode.com/svn/trunk/addons/','statsUrl' => '', 'xmlUrl' => 'http://kozz-addons.googlecode.com/svn/trunk/addons/addons.xml', 'repo_id' => 'repository.googlecode.kozz-addons', 'zip' => '1', 'downloadUrl' => 'http://kozz-addons.googlecode.com/svn/trunk/addons/repository.googlecode.kozz-addons/repository.googlecode.kozz-addons-2.0.9.zip' )

	),
	// template and rendering related settings
	'templatePath' => 'templates',
	'images' => array(
		'dummy' => 'images/addon-dummy.png',
		'sizes' => array(
			'addonThumbnail' => array(120,120),
			'addonThumbnailSmall' => array(60,60),
			'large' => array(256,256)
		)
	),
	'analytics' => "<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-51395931-1', 'auto');
  ga('send', 'pageview');

</script>",
//	'addonExcludeClause' => ' AND NOT deleted AND id NOT LIKE "%.common.%" AND id NOT LIKE "script.module%" ',
	'categories' => array(
		'All' => array(
			'label' => 'All Add-ons',
		),
		'categories2' => array(
			'label' => 'Categories',
			'subCategories' => array(
				'audio' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'contentType' => 'audio',
					'label' => 'Audio'
				),
				'video' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'contentType' => 'video',
					'label' => 'Video'
				),
				'pictures' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'contentType' => 'image',
					'label' => 'Pictures'
				),
				'screensaver' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'contentType' => 'screensaver',
					'label' => 'Screensaver'
				),
				'skins' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.gui.skin',
					'label' => 'Skins'
				),
				'weather' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.python.weather',
					'label' => 'Weather'
				),
				'programs' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'contentType' => 'executable',
					'label' => 'Programs'
				),
				'lyrics' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.python.lyrics',
					'label' => 'Lyrics'
				),
				'webinterface' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.gui.webinterface',
					'label' => 'Webinterface'
				),
				'metadata' => array(
					'extensionPoint' => 'xbmc.metadata',
					'label' => 'Metadata',
					'subCategories' => array(
						'artists' => array(
							'not_adult' => 'yes',
							'depreciated' => '',
							'extensionPoint' => 'xbmc.metadata.scraper.artists',
							'label' => 'Artists'
						),
						'albums' => array(
							'not_adult' => 'yes',
							'depreciated' => '',
							'extensionPoint' => 'xbmc.metadata.scraper.albums',
							'label' => 'Albums'
						),
						'movies' => array(
							'not_adult' => 'yes',
							'depreciated' => '',
							'extensionPoint' => 'xbmc.metadata.scraper.movies',
							'label' => 'Movies'
						),
						'musicvideos' => array(
							'not_adult' => 'yes',
							'depreciated' => '',
							'extensionPoint' => 'xbmc.metadata.scraper.musicvideos',
							'label' => 'Musicvideos'
						),
						'tvshows' => array(
							'not_adult' => 'yes',
							'depreciated' => '',
							'extensionPoint' => 'xbmc.metadata.scraper.tvshows',
							'label' => 'TV-Shows'
						),
					)
				),
				'subtitles' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.python.subtitles',
					'label' => 'Subtitles'
				),
				'services' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.service',
					'label' => 'Services'
				),
				'scriptmodules' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'extensionPoint' => 'xbmc.python.module',
					'label' => 'Script Modules'
				),
			),
		),
		'genres' => array(
			'label' => 'Genre Specific',
			'subCategories' => array(
				'anime' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'anime',
					'label' => 'Anime'
				),
				'audiobooks' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'audiobooks',
					'label' => 'Audiobooks'
				),
				'comedy' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'comedy',
					'label' => 'Comedy'
				),
				'comics' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'comics',
					'label' => 'Comics'
				),
				'documentary' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'documentary',
					'label' => 'Documentary'
				),
				'downloads' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'downloads',
					'label' => 'Downloads'
				),
				'food' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'food',
					'label' => 'Food'
				),
				'gaming' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'gaming',
					'label' => 'Gaming'
				),
				'health' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'health',
					'label' => 'Health'
				),
				'howto' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'howto',
					'label' => 'How To...'
				),
				'kids' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'kids',
					'label' => 'Kids'
				),
				'livetv' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'livetv',
					'label' => 'Live TV'
				),
				'movies' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'movies',
					'label' => 'Movies'
				),
				'music' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'music',
					'label' => 'Music'
				),
				'news' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'news',
					'label' => 'News & Weather'
				),
				'photos' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'photos',
					'label' => 'Photos'
				),
				'podcasts' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'podcasts',
					'label' => 'Podcasts'
				),
				'radio' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'radio',
					'label' => 'Radio'
				),
				'religion' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'religion',
					'label' => 'Religion'
				),
				'space' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'space',
					'label' => 'Space'
				),
				'sports' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'sports',
					'label' => 'Sports'
				),
				'tech' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'tech',
					'label' => 'Technology'
				),
				'trailers' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'trailers',
					'label' => 'Trailers'
				),
				'tv' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'tv',
					'label' => 'TV Shows'
				),
				'adult' => array(
					'depreciated' => '',
					'genreType' => 'adult',
					'label' => 'XXX'
				),
				'other' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'other',
					'label' => 'Misc.'
				),
			),
		),
		'countries' => array(
			'label' => 'Regional',
			'subCategories' => array(
				'african' => array(
					'contentType' => 'video',
					'genreType' => 'african',
					'label' => 'African'
				),
				'arabic' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'arabic',
					'label' => 'Arabic'
				),
				'asian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'asian',
					'label' => 'Asian'
				),
				'australian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'australian',
					'label' => 'Australian'
				),
				'austrian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'austrian',
					'label' => 'Austrian'
				),
				'belgian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'belgian',
					'label' => 'Belgian'
				),
				'brazilian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'brazilian',
					'label' => 'Brazilian'
				),
				'canadian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'canadian',
					'label' => 'Canadian'
				),
				'chinese' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'chinese',
					'label' => 'Chinese'
				),
				'columbian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'columbian',
					'label' => 'Columbian'
				),
				'croatian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'croatian',
					'label' => 'Croatian'
				),
				'czech' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'czech',
					'label' => 'Czech'
				),
				'danish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'danish',
					'label' => 'Danish'
				),
				'dominican' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'dominican',
					'label' => 'Dominican'
				),
				'dutch' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'dutch',
					'label' => 'Dutch'
				),
				'egyptian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'egyptian',
					'label' => 'Egyptian'
				),
				'filipino' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'filipino',
					'label' => 'Filipino'
				),
				'finnish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'finnish',
					'label' => 'Finnish'
				),		
				'french' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'french',
					'label' => 'French'
				),
				'german' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'german',
					'label' => 'German'
				),
				'greek' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'greek',
					'label' => 'Greek'
				),
				'hebrew' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'hebrew',
					'label' => 'Hebrew'
				),
				'hungarian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'hungarian',
					'label' => 'Hungarian'
				),
				'icelandic' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'icelandic',
					'label' => 'Icelandic'
				),
				'indian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'indian',
					'label' => 'Indian'
				),
				'irish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'irish',
					'label' => 'Irish'
				),
				'italian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'italian',
					'label' => 'Italian'
				),
				'japanese' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'japanese',
					'label' => 'Japanese'
				),		
				'korean' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'korean',
					'label' => 'Korean'
				),
				'lebanese' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'lebanese',
					'label' => 'Lebanese'
				),
				'mongolian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'mongolian',
					'label' => 'Mongolian'
				),
				'moroccan' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'moroccan',
					'label' => 'Moroccan'
				),
				'nepali' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'nepali',
					'label' => 'Nepali'
				),
				'newzealand' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'newzealand',
					'label' => 'New Zealand'
				),
				'norwegian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'norwegian',
					'label' => 'Norwegian'
				),
				'pakistani' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'pakistani',
					'label' => 'Pakistani'
				),
				'polish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'polish',
					'label' => 'Polish'
				),
				'portuguese' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'portuguese',
					'label' => 'Portuguese'
				),
				'romanian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'romanian',
					'label' => 'Romanian'
				),
				'russian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'russian',
					'label' => 'Russian'
				),		
				'singapore' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'singapore',
					'label' => 'Singapore'
				),
				'spanish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'spanish',
					'label' => 'Spanish'
				),
				'swedish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'swedish',
					'label' => 'Swedish'
				),
				'swiss' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'swiss',
					'label' => 'Swiss'
				),
				'syrian' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'syrian',
					'label' => 'Syrian'
				),
				'tamil' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'tamil',
					'label' => 'Tamil'
				),
				'thai' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'thai',
					'label' => 'Thai'
				),
				'turkish' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'turkish',
					'label' => 'Turkish'
				),
				'uk' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'uk',
					'label' => 'UK'
				),
				'usa' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'usa',
					'label' => 'USA'
				),
				'vietnamese' => array(
					'not_adult' => 'yes',
					'depreciated' => '',
					'genreType' => 'vietnamese',
					'label' => 'Vietnamese'
				),
			),
		),
		'repositories' => array(
			'not_adult' => 'yes',
			'depreciated' => '',
			'extensionPoint' => 'xbmc.addon.repository',
			'contentType' => 'repository',
			'label' => 'Repositories'
		),
		'broken' => array(
			'depreciated' => '',
			'broken_addons' => '',
			'label' => 'Broken Addons'
		),
		'graveyard' => array(
			'depreciated' => '1',
			'label' => 'Graveyard'
		),
		'xbox' => array(
			'label' => 'Xbox Original',
			'subCategories' => array(
				'audio' => array(
					'depreciated' => '',
					'contentType' => 'audio',
					'xboxCompatible' => 'yes',
					'label' => 'Audio'
				),
				'video' => array(
					#'extensionPoint' => 'xbmc.python.pluginsource',
					'depreciated' => '',
					'contentType' => 'video',
					'xboxCompatible' => 'yes',
					'label' => 'Video'
				),
				'pictures' => array(
					#'extensionPoint' => 'xbmc.python.pluginsource',
					'depreciated' => '',
					'contentType' => 'image',
					'xboxCompatible' => 'yes',
					'label' => 'Pictures'
				),
				'programs' => array(
					#'extensionPoint' => 'xbmc.python.pluginsource',
					'depreciated' => '',
					'contentType' => 'executable',
					'xboxCompatible' => 'yes',
					'label' => 'Programs'
				),
				'skins' => array(
					'depreciated' => '',
					'xboxCompatible' => 'yes',
					'extensionPoint' => 'xbmc.gui.skin',
					'label' => 'Skins'
				),
			),
		),	
		'xboxtesting' => array(
			'label' => 'Need Testing',
			'subCategories' => array(
				'audio' => array(
					'xbox_untested' => '1',
					'depreciated' => '',
					'contentType' => 'audio',
					'label' => 'Audio'
				),
				'video' => array(
					'xbox_untested' => '1',
					'depreciated' => '',
					'contentType' => 'video',
					'label' => 'Video'
				),
				'pictures' => array(
					'xbox_untested' => '1',
					'depreciated' => '',
					'contentType' => 'image',
					'label' => 'Pictures'
				),
				'programs' => array(
					'xbox_untested' => '1',
					'depreciated' => '',
					'contentType' => 'executable',
					'label' => 'Programs'
				),
			),
		),
	
	),	
	// cache settings
	'cache' => array(
		'pathWrite' => SITE_ROOT . 'cache' . DIRECTORY_SEPARATOR,
		'pathRead' => 'cache/'
	),
	'baseUrl' => NULL,
	'security' => array(
		'token' => ''
	)
);


// include the context depending configuration at the bottom
// which allows to override any default configuration if needed
if (CONTEXT == 'development') {
	require_once('developmentConfiguration.php');
} else {
	require_once('/etc/xbmc/php-include/addons/private/configuration.php');
}
?>