const fs = require('fs')

const db = require('./script')


let plantsData

const getplants = async () => {
    const headers = {
        "X-RapidAPI-Key": "0c50584d72msh7b3c59e3638f72cp19c2d4jsn4aa5ee1658e6",
        "X-RapidAPI-Host": "house-plants.p.rapidapi.com"
    }

    const options = {
        method: "GET",
        headers: headers
    }

    const resp = await fetch("https://house-plants.p.rapidapi.com/all", options)
    plantsData = await resp.json()
    }

const addData = async (a, b) => {


    console.log(plantsData)
    plantsData.forEach( async (plant, index) => {
        if (index >= a && index <= b) {
        // Add plant to db
        const {category, climate, ideallight, latin, origin, toleratedlight, watering} = plant
        const max_temp = plant.tempmax.celsius
        const min_temp = plant.tempmin.celsius
        console.log(min_temp, max_temp)
        let pests
        if (Array.isArray(plant.insects)) {
             pests = plant.insects.flat()
            }
        else {
            pests = plant.insects
        }

        const names = plant.common.flat()
        await db.query("INSERT INTO plant__data (category, names, latin_name, min_temp, max_temp, ideal_light, tolerated_light, pests, watering, origin, climate) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)", [category, names, latin , min_temp, max_temp, ideallight, toleratedlight, pests, watering, origin, climate]);
    }
    })
}





const addToDB = async () => {


  await getplants()
  
    // for (let i = 0; i < 210; i += 5) {
    //         console.log(i + "to" + (i+4))
    //         await addData(i, i+4)

    // } 
    await addData(5,9)

}


addToDB()
