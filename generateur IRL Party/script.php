<?php

use EscapeGame\Database;

require_once 'lib/autoload.php';

$faker = Faker\Factory::create();
$escapegame = new Database();

if (empty($argv[1]) == true) {
    $timer = 1000000;
} else {
    $timer = $argv[1]*1000;
}


while (true) {
    usleep($timer);
    $firstAge = $escapegame->getAge();
    $nbTickets = $escapegame->getNbTickets();
    $firstCivility = $escapegame->getGender(false);
    $firstNom = $faker->firstName;
    $firstPrenom = $faker->firstName;
    $firstEmail = $firstNom . '.' . $firstPrenom . '@' . $escapegame->getSuffixEmail();
    $firstPersonType = $escapegame->getPersonType($firstAge);

    $result['Acheteur']['Civilite'] = $firstCivility;
    $result['Acheteur']['Nom'] = $firstNom;
    $result['Acheteur']['Prenom'] = $firstPrenom;
    $result['Acheteur']['Age'] = $firstAge;
    $result['Acheteur']['Email'] = strtolower($firstEmail);
    $result['Game']['Nom'] = $escapegame->getEscapeGameName();
    $result['Game']['Jour'] = $escapegame->getReservationDate();
    $result['Game']['Horaire'] = $escapegame->getReservationHour();
    $result['Game']['VR'] = $escapegame->useVirtualReality();
    $result['Game']['Themes'] = $escapegame->getThemes($result['Game']['Nom']);
    for ($i = 0; $i < $nbTickets; $i++) {
        if ($i == 0) {
            $result['Reservation'][$i]['Spectateur']['Civilite'] = $firstCivility;
            $result['Reservation'][$i]['Spectateur']['Nom'] = $firstNom;
            $result['Reservation'][$i]['Spectateur']['Prenom'] = $firstPrenom;
            $result['Reservation'][$i]['Spectateur']['Age'] = $firstAge;
            $result['Reservation'][$i]['Tarif'] = $firstPersonType;
        } else {
            $otherAge = $escapegame->getAge();
            $otherCivility = $escapegame->getGender(false);
            $otherNom = $faker->firstName;
            $otherPrenom = $faker->firstName;
            $otherPersonType = $escapegame->getPersonType($otherAge);

            $result['Reservation'][$i]['Spectateur']['Civilite'] = $otherCivility;
            $result['Reservation'][$i]['Spectateur']['Nom'] = $otherNom;
            $result['Reservation'][$i]['Spectateur']['Prenom'] = $otherPrenom;
            $result['Reservation'][$i]['Spectateur']['Age'] = $otherAge;
            $result['Reservation'][$i]['Tarif'] = $otherPersonType;
        }
    }




    $curl = curl_init();

    $json = json_encode($result);

    curl_setopt_array($curl, array(
      CURLOPT_PORT => "8000",
      CURLOPT_URL => "http://127.0.0.1:8000/api/v1/reservation",
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_ENCODING => "",
      CURLOPT_MAXREDIRS => 10,
      CURLOPT_TIMEOUT => 30,
      CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
      CURLOPT_CUSTOMREQUEST => "POST",
      CURLOPT_POSTFIELDS => $json,
      CURLOPT_HTTPHEADER => array(
        "Content-Type: application/json",
        "cache-control: no-cache"
      ),
    ));

    $response = curl_exec($curl);
    $err = curl_error($curl);

    curl_close($curl);

    if ($err) {
      echo "cURL Error #:" . $err . "\n";
    } else {
      echo $response . "\n";
    }

}
