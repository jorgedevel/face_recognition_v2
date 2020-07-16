const { spawn } = require('child_process')
const express = require('express')
const cors = require('cors')
const app = express()

app.use(cors())
app.use(express.json())

app.post('/api/exec/register', (req, res) => {
    const {
        name,
        lastname
    } = req.body;

    const programPython = spawn('py', ['register.py', name, lastname])

    programPython.stdout.on('data', (data) => {
        //res.write(data)
        console.log(data.toString())
    })

    programPython.on('close', (code) => {
        console.log(`python program exit with code ${code}`)
        res.end()
    })
})

app.post('/api/exec/recognize', (req, res) => {
    const {
        name,
        lastname
    } = req.body;

    const programPython = spawn('py', ['recognize.py', name, lastname])

    programPython.stdout.on('data', (data) => {
        //res.write(data)
        console.log(data.toString())
    })

    programPython.on('close', (code) => {
        console.log(`python program exit with code ${code}`)
        res.end()
    })
})

app.listen(3000, () => {
    console.log('server run')
})
