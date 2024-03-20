import express from 'express'

const app = express()
const port = 8080

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.post('/webhook', (req, res) => {
    console.log('New data from webhook:', req.body)
    res.status(200)
})

app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`)
})