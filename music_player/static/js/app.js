var app = new Vue({
  el: '#music',
  data: {
    artists: [],
    artist: ''
  },
  created: function () {
    var self = this;
    axios.get('artists')
    .then(function(response) {
      self.artists = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });
  },
  methods: {
    playAlbum: function(id) {
      axios.get('albums/' + id)
      .catch(function (error) {
        console.log(error);
      });
    },
    getArtist: function(id) {
      var self = this;
      axios.get('artists/' + id)
        .then(function (response) {
        self.$data.artist = response.data;
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    playSong: function(id) {
      axios.get('songs/' + id)
      .then(function (response) {
    })
    .catch(function(error) {
      console.log(error);
     });
    }
  }
})
